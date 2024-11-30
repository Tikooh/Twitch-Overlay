import sys
import requests
from dotenv import load_dotenv
import os
import datetime
import json
from types import SimpleNamespace
import client
import asyncio

load_dotenv()

CLIENT_ID = os.getenv("EVENTSUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("EVENTSUB_CLIENT_SECRET")

def parse_message(msg):
    obj = json.loads(msg)
    metadata = obj["metadata"]
    payload = obj["payload"]
    return Message(metadata, payload)

class Message(object):
    def __init__(self, metadata, payload):
        self.metadata = metadata
        self.kind = self.message_type()

        payloadLayer1 = {}
        for k, v in payload.items():
            payloadLayer1[k] = SimpleNamespace(**v)
        self.payload = SimpleNamespace(**payloadLayer1)

    def message_id(self):
        return self.metadata["message_id"]
    def message_type(self):
        return self.metadata["message_type"]
    def message_timestamp(self):
        return self.metadata["message_timestamp"]
    

class Auth(object):
    def __init__(self, token, valid_until):
        self.token = token
        self.valid_until = valid_until
    
    def is_valid(self):
        return datetime.now() > self.valid_until
    
    def get_bearer_token(self):
        print(auth.token)
        return "Bearer " + auth.token


def get_auth():
    res = requests.post("https://id.twitch.tv/oauth2/token", data= {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })

    if res.status_code == 200:
        body = res.json()
        if body["token_type"] != "bearer":
            raise Exception(f"Did not receive correct token type")
        valid_until = datetime.datetime.now() + datetime.timedelta(seconds=body["expires_in"])
        return Auth(body["access_token"], valid_until)
    
if __name__ == "__main__":
    load_dotenv()
    auth = get_auth()
    asyncio.run(client.init(auth))