import asyncio
import aiohttp
import json
import os
import re 

from waypoint import WaypointSession


async def main():

    with open('config.json', 'r') as file:
        config = json.load(file)

    username = config['username']
    password = config['password']

    ws = await WaypointSession().login(username, password)

    # resp = await ws.H5.request(
    #     'POST',
    #     "https://ugc.svc.halowaypoint.com/h5/players/xuid(2533274983464522)/bookmarks?auth=st",
    #     headers={
    #         'X-343-Authorization-Spartan': ws.v3_token,
    #         'Content-Type': 'application/json'
    #     },
    #     data=json.dumps({
    #         'Name': 'Cryptum - MapVariant',
    #         'Description': 'cryptum-halodotapi',
    #         'AccessControl': 0,
    #         'Target': {
    #             'ResourceId': "34f50bf5-3457-4c9f-9215-4da0af6fc54d",
    #             'ResourceType': 'MapVariant',
    #             'Owner': 'Bighossbagel',
    #             'OwnerType': 'UgcPlayer'
    #         }
    #     })
    # )
    # if resp.status == 200:
    #     print(await resp.json())

    async with ws.H5.ContentHacs_FlexibleStats(startat="0", count='10').get() as resp:
        with open("result.json", 'w') as file:
            json.dump(await resp.json(), file, indent=4)


    await ws.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())