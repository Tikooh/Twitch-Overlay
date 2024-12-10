from twitchAPI.twitch import Twitch

from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import ChannelFollowEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope
import asyncio
from dotenv import load_dotenv
import os
import ssl
import json
from chatbot import send_to_clients

import logging


logging.basicConfig(level=logging.DEBUG)

load_dotenv()
clients = set()

APP_ID = os.getenv("EVENTSUB_CLIENT_ID")
APP_SECRET = os.getenv("EVENTSUB_CLIENT_SECRET")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS]


async def on_follow(data: ChannelFollowEvent):
    # our event happened, lets do things with the data we got!
    print(f'{data.event.user_name} now follows {data.event.broadcaster_user_name}!')
    await send_to_clients('follow', data.event)


async def run():
    # create the api instance and get user auth either from storage or website
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()

    # get the currently logged in user
    user = await first(twitch.get_users())

    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    # subscribing to the desired eventsub hook for our user
    # the given function (in this example on_follow) will be called every time this event is triggered
    # the broadcaster is a moderator in their own channel by default so specifying both as the same works in this example
    # We have to subscribe to the first topic within 10 seconds of eventsub.start() to not be disconnected.
    await eventsub.listen_channel_follow_v2(user.id, user.id, on_follow)

    # eventsub will run in its own process
    # so lets just wait for user input before shutting it all down again
    try:
        input('press Enter to shut down...')
    except KeyboardInterrupt:
        pass
    finally:
        # stopping both eventsub as well as gracefully closing the connection to the API
        await eventsub.stop()
        await twitch.close()

if __name__ == "__main__":
    asyncio.run(run())
