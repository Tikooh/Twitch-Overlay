import asyncio
from websockets.asyncio.client import connect
from eventsub import parse_message
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def enable_all_subscriptions(auth, session_id):
    enable_subscription(auth, session_id, "channel.follow", {
        "broadcaster_user_id": 213205254,
        "moderator_user_id": 213205254,
    })


def enable_subscription(sessionID, auth, sub_type, condition):
    res = requests.post(data={
        "type": sub_type,
        "version": 1,
        "condition": condition,
        "transport": {
            "method": "websocket",
            "session_id": sessionID,
        }
    }, headers= {
        "Authorization": auth.get_bearer_token(),
        "Client-Id": os.getenv('CLIENT_ID'),
        "Content-Type": "application/json",
    })

    if res.status_code != 200:
        raise Exception("Failed to request subscription")
    
async def init(auth):
    async with connect("wss://eventsub.wss.twitch.tv/ws", additional_headers = {"Authorization": auth.get_bearer_token()}) as ws:
        msg = await ws.recv()
        msg = parse_message(msg)
        if msg.kind != "session_welcome":
            raise Exception("first message must be welcome")
        print("handshake successful")
        sessionID = msg.payload.session.id
        enable_all_subscriptions(sessionID, auth)
        await ws.close()

