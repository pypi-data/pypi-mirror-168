import asyncio
import aiohttp
import re
import json


RELYING_PARTY = "https://prod.xsts.halowaypoint.com/"

# TODO: Token refreshing


# Initiates an XBL login process on behalf of halowaypoint,
# returning a redirect URL to XBL login page.
#
# [ Deprecated in favour of XSTS auth. ]
async def xblive_redirect_url(session) -> str:
    WAYPOINT_SIGNIN = "https://www.halowaypoint.com/sign-in"

    async with session.get(WAYPOINT_SIGNIN, allow_redirects=False) as resp:
        if resp.status != 302:
            raise Exception(
                f"Could not retrieve login redirect url:\n{await resp.text()}"
            )
        login_redirect_url = dict(resp.headers)['Location']

    return login_redirect_url


# Extracts and returns the PPFT and the post URL for user credentials, 
# from the halowaypoint login redirect URL.
async def ppft_and_post(session, response_type, login_redirect_url=None) -> (str, str):
    PPFT_RE = r"<input type=\"hidden\" name=\"PPFT\" id=\"i0327\" value=\"(.*?)\"/>"
    POST_RE = r"urlPost: ?'(.*?)'"

    if response_type == 'token':
        login_redirect_url = "https://login.live.com/oauth20_authorize.srf?" + \
            f"response_type={response_type}&" + \
            "redirect_uri=https://login.live.com/oauth20_desktop.srf&" + \
            "scope=service::user.auth.xboxlive.com::MBI_SSL&" + \
            "client_id=000000004C12AE6F"

    # print(login_redirect_url, '\n')

    async with session.get(login_redirect_url, allow_redirects=False) as resp:
        if resp.status != 200:
            raise Exception(
                f"Could not retrieve PPFT and postURL:\n{await resp.text()}"
            )
        resp_text = await resp.text()

        ppft = re.search(PPFT_RE, resp_text).group(1)
        login_post_url = re.search(POST_RE, resp_text).group(1)

    return ppft, login_post_url


# Posts user credentials and the previously extracted PPFT to the login URL,
# returning a halowaypoint callback URL.
async def live_login(session, post_url, ppft, username, password) -> str:
    data = {
        'login':  username,
        'loginfmt': username,
        'passwd': password,
        'PPFT':   ppft,
    }

    async with session.post(post_url, data=data, allow_redirects=False, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    }) as resp:

        if resp.status != 302:
            raise Exception(
                f"Could not log in:\n{await resp.text()}"
            )
        callback_url = dict(resp.headers)['Location']

        if 'access_token' in callback_url:
            rps_ticket = callback_url.split('access_token=')[1].split('&')[0]

            return rps_ticket

    return callback_url


async def get_user_token(session, rps_ticket) -> str:
    url = "https://user.auth.xboxlive.com/user/authenticate"

    data = json.dumps({
        'RelyingParty': 'http://auth.xboxlive.com',
        'TokenType': 'JWT',
        'Properties': {
            'AuthMethod': 'RPS',
            'SiteName': 'user.auth.xboxlive.com',
            'RpsTicket': f"t={rps_ticket}"
        }
    })
    
    async with session.post(url, data=data, allow_redirects=False, headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }) as resp:
        if resp.status != 200:
            raise Exception(
                f"Could not retrieve User Token:\n{resp}"
            )

        token = (await resp.json())['Token']

    return token


async def get_xsts_token(session, user_token, relying_party=RELYING_PARTY):
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"

    data = json.dumps({
        'RelyingParty': relying_party,
        'TokenType': 'JWT',
        'Properties': {
            'UserTokens': [user_token],
            'SandboxId': 'RETAIL'
        }
    })

    async with session.post(url, data=data, allow_redirects=False, headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }) as resp:
        if resp.status != 200:
            raise Exception(
                f"Could not retrieve XSTS Token:\n{resp}"
            )
            
        token = (await resp.json())['Token']

    return token


async def get_v4_token(session, xbl3_authorization) -> str:
    url = "https://settings.svc.halowaypoint.com/spartan-token"

    async with session.post(
        url, 
        headers={
            'Accept': 'application/json'
        },
        json={
            "Audience": "urn:343:s3:services",
            "MinVersion": "4",
            "Proof": [
                {
                    "Token": xbl3_authorization,
                    "TokenType": "Xbox_XSTSv3"
                }
            ]
        }
    ) as resp:
        v4_token = (await resp.json())['SpartanToken']

    return v4_token


async def get_v3_token(session, xbl3_authorization) -> str:
    url = "https://settings.svc.halowaypoint.com/spartan-token?v=3"

    async with session.get(
        url, 
        headers={
            "X-343-Authorization-XBL3": f"XBL3.0 x=*;{xbl3_authorization}",
            'Accept': 'application/json'
        }
    ) as resp:
        v3_token = (await resp.json())['SpartanToken']

    return v3_token


# Extracts and returns additional 343-clearance, needed for accessing certain
# features of the halowaypoint API. The clearance is not set as a permanent
# header because some endpoints do not work with it present.
# 
# A user XUID or Gamer Tag must be provided that matches the account used 
# when retrieving the spartan_token.
#
# Spartan_token does not need to be provided as long as the session headers 
# already contain a valid spartan_token.
async def get_343_clearance(session, v4_token, xuid=None, gt=None) -> str:
    if not xuid and not gt:
        raise Exception("User XUID or GamerTag required")

    url = f"https://halostats.svc.halowaypoint.com/hi/players/{gt or f'xuid({xuid})'}/decks"
    headers = {
        'Accept': "application/json",
        'Referer': "https://www.halowaypoint.com/",
        'x-343-authorization-spartan': v4_token
    }

    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            raise Exception(
                f"Could not retrieve 343-clearance:\n{await resp.text()}"
            )
        clearance = (await resp.json())['ClearanceId']

    return clearance


async def login(email, password, tokens=['v3', 'v4'], session=None) -> [str]:
    if not session: 
        session = aiohttp.ClientSession()

    ppft, post_url = await ppft_and_post(session, 'token')
    rps_ticket     = await live_login(session, post_url, ppft, email, password)
    user_token     = await get_user_token(session, rps_ticket)
    xsts_token     = await get_xsts_token(session, user_token)

    _tokens = []

    for token in tokens:
        if token == 'v3':
            _tokens.append(await get_v3_token(session, xsts_token))

        elif token == 'v4':
            _tokens.append(await get_v4_token(session, xsts_token))

    return _tokens
