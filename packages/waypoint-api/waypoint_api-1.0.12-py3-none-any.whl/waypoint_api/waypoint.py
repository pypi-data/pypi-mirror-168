import aiohttp
import logging
import os
import json
import re

from .auth_flow import login, get_343_clearance

# https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48
with open(os.path.dirname(__file__) + "/endpoints/hi.json", 'r') as file:
    hi_endpoints = json.load(file) 

HI_AUTHORITIES = hi_endpoints['Authorities']
HI_ENDPOINTS   = hi_endpoints['Endpoints'] 

# https://settings.svc.halowaypoint.com/settings/h5pc/a1b344c4-91a3-47f7-92f4-95784cda3cd2
# all references to H5PC have been changed to H5
with open(os.path.dirname(__file__) + "/endpoints/h5.json", 'r') as file:
    h5_endpoints = json.load(file) 

H5_AUTHORITIES = h5_endpoints['Authorities']
H5_ENDPOINTS   = h5_endpoints['Endpoints'] 


class User:

    def __init__(self, gamertag=None, xuid=None):
        self._gamertag = gamertag
        self._xuid = xuid

    @property
    def gamertag(self):
        return self._gamertag

    @property
    def xuid(self):
        return f"xuid({self._xuid})"


class WaypointSession:

    def __init__(self, headers=None):

        if not headers:
            headers = {}

        # All API calls pass and return JSON content-type by defualt.
        # This can be changed by passing additional headers to 
        # WaypointRequest REST calls (see WaypointRequest class).
        self.session = aiohttp.ClientSession(
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                # Halo: Infinite PC
                # 'User-Agent': "SHIVA-2043073184/6.10021.18539.0 (release; PC)",
                # Halo 5: Forge PC
                # 'User-Agent': "cpprestsdk/2.4.0",
                **headers
            }
        ) 

        self._username: str = None
        self._password: str = None
        
        self.user = User()

        self._v4_token: str = None
        self._v3_token: str = None
        self._343_clearance: str = None

        self.authorities: dict = None
        self.endpoints: dict = None
    
    @property
    def H5(self):
        self.session.headers['x-343-authorization-spartan'] = self.v3_token
        self.authorities = H5_AUTHORITIES
        self.endpoints   = H5_ENDPOINTS
        return self

    @property
    def HI(self):
        self.session.headers['x-343-authorization-spartan'] = self.v4_token
        self.authorities = HI_AUTHORITIES
        self.endpoints   = HI_ENDPOINTS
        return self

    @property
    def v4_token(self):
        return self._v4_token

    @property
    def v3_token(self):
        return self._v3_token

    @property
    def clearance(self):
        return self._343_clearance

    # At the time of writing this, the flightId is equivalent to clearanceId.
    # This might change in the future, if so, flightId can be extracted from
    # Settings_ActiveFlight endpoint (see api_source.json).
    @property
    def flight(self):
        return self._343_clearance

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_, **__):
        await self.close()

    async def close(self):
        await self.session.close()

    # Wrapper around a aiohttp.ClientSession request.
    async def request(self, method, url, *_, **kwargs) -> aiohttp.ClientResponse:
        resp = await self.session.request(method, url, **kwargs)

        if (resp.status) == 200:
            print(f"[ {resp.status} ] {method} {url}")
        else:
            print(f"[ {resp.status} ] {method} {url}\n{await resp.text()}")

        return resp

    # Attempts to log in to waypoint servers using given user credentials.
    # Sets _v3_token, _v4_token and _343_clearance if successful.
    async def login(self, username, password):
        self._username = username
        self._password = password

        self._v3_token, self._v4_token = await login(
            username, 
            password,
            tokens=['v3', 'v4'],
            session=self.session
        )

        async with self.HI.Profile_GetUserInfo().get(
            headers={
                'Accept': 'application/json'
            }
        ) as resp:
            user_info = await resp.json()
            self.user = User(user_info['gamertag'], user_info['xuid'])

        self._343_clearance = await get_343_clearance(
            self.session, v4_token=self.v4_token, gt=self.user.gamertag
        )

        print(f"Logged in as '{self.user.gamertag} ({self.user._xuid})'")

        return self


    # Looks up the authority corresponding to the requested endpoint.
    # Sets 343-clearance header if the endpoint requires it.
    def prepare_url_and_headers(self, endpoint) -> (str, dict):
        authority = self.authorities[endpoint['AuthorityId']]

        url = 'https://' + authority['Hostname'] + endpoint['Path'] + endpoint['QueryString']

        if (endpoint['ClearanceAware']):
            return url, {'343-clearance': self._343_clearance}

        return url, {}

    # Helper function to pass keyword arguments into the URL.
    # All excess keyword arguments will be appeneded as the URL query string.
    def format_url(self, endpoint, url, *_, **kwargs) -> str:
        def repl(match):
            group = match.group(1)

            if group in ('flightId', 'clearanceId') and group not in kwargs:
                val = self._343_clearance 
            else:
                val = kwargs[group]

            if group in kwargs:
                del kwargs[group]

            return val

        fmt_url = re.sub(pattern=r"{(.*?)}", repl=repl, string=url)
        
        if kwargs:
            if endpoint['QueryString']:
                fmt_url += '&'
            else:
                fmt_url += '?'

        fmt_url += '&'.join(f"{k}={v}" for k, v in kwargs.items())

        return fmt_url

    # Allows for access to all endpoints specified in "h5.json" and "hi.json".
    # Returns WaypointRequest.
    #
    # Example:
    # ws = WaypointSession()
    # await ws.login( ... )
    # match_history = await ws.Stats_GetMatchHistory(player="Fliqqr").get()
    #
    def __getattr__(self, attr):
        if not (endpoint := self.endpoints.get(attr)):
            raise Exception(
                f"No known endpoint '{attr}'"
            )
        url, headers = self.prepare_url_and_headers(endpoint)

        def func(*args, **kwargs) -> WaypointRequest:
            try:    
                fmt_url = self.format_url(endpoint, url, *args, **kwargs)

            except KeyError as arg:
                raise Exception(
                    f"Missing required argument {arg} in method \'{attr}\' " + \
                    json.dumps(endpoint, indent=4)
                )
            return WaypointRequest(self, fmt_url, headers=headers)

        return func


# Wrapper around HaloWaypoint API and aiohttp request.
# Exposes basic REST methods for communicating with the API.
# 
# Methods can be called directly:
# 
# resp = await WaypointRequest.get(...)
# data = await resp.json()
#
# Or using context manager:
# 
# async with WaypointRequest.get(...) as resp:
#       data = await resp.json()
#
class WaypointRequest:

    allowed_methods = {
        'get': 'GET',
        'post': 'POST',
        'delete': 'DELETE'
    }

    def __init__(self, waypoint_session: WaypointSession, *args, **kwargs):
        self.waypoint_session = waypoint_session
        self.args   = args
        self.kwargs = kwargs

        self.method: str = None
        self.open_request: aiohttp.ClientResponse = None

    def __await__(self) -> aiohttp.ClientResponse:
        if not self.method:
            raise Exception("No request method specified")

        return self.waypoint_session.request(
            self.method, *self.args, **self.kwargs
        ).__await__()

    async def __aenter__(self) -> aiohttp.ClientResponse:
        if not self.method:
            raise Exception("No request method specified")
            
        self.open_request = await self.waypoint_session.request(
            self.method, *self.args, **self.kwargs
        )
        return self.open_request

    async def __aexit__(self, *_, **__):
        self.open_request.close()

    def __del__(self):
        if self.open_request:
            self.open_request.close()

    def _prep_request(self, method, *args, **kwargs):
        self.method = method
        self.args = (*self.args, *args)
        self.kwargs = {**self.kwargs, **kwargs}
        return self

    # def __getattr__(self, attr):
    #     return 

    def get(self, *args, **kwargs):
        return self._prep_request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._prep_request('POST', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._prep_request('DELETE', *args, **kwargs)
    