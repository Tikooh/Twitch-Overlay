import asyncio
from websockets.asyncio.client import connect
from eventsub import parse_message
import requests
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("EVENTSUB_CLIENT_ID")
print(CLIENT_ID)
CLIENT_SECRET = os.getenv("EVENTSUB_CLIENT_SECRET")

def enable_all_subscriptions(auth, session_id, version):
    print(f"Subscribing to event channel.follow")
    enable_subscription(auth, session_id, "channel.follow", {
        "broadcaster_user_id": "213205254",
        "moderator_user_id": "213205254",
    }, version=version)


def enable_subscription(sessionID, auth, sub_type, condition, version):
    res = requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", json={
        "type": sub_type,
        "version": version,
        "condition": condition,
        "transport": {
            "method": "websocket",
            "session_id": sessionID,
        }
    }, headers= {
        "Authorization": auth.get_bearer_token(),
        "Client-Id": CLIENT_ID,
        "Content-Type": "application/json",
    })

    if res.status_code != 200:
        print(auth.get_bearer_token())
        print(res.json())
        print(sessionID)
        print(os.getenv("CLIEENT_ID"))
        raise Exception("Failed to request subscription")
    
async def init(auth):
    async with connect("wss://eventsub.wss.twitch.tv/ws", additional_headers = {"Authorization": auth.get_bearer_token()}) as ws:
        msg = await ws.recv()
        msg = parse_message(msg)
        if msg.kind != "session_welcome":
            raise Exception("first message must be welcome")
        print("handshake successful")
        sessionID = msg.payload.session.id
        enable_all_subscriptions(sessionID, auth, 2)
        await ws.close()

