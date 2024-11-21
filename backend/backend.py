import os
import websockets
from dotenv import load_dotenv
from twitchio.ext import commands, eventsub
import json
import asyncio
import logging
import ssl

logging.basicConfig(level=logging.DEBUG)


# FOR EVENTS CONFIGURE NGINX AT /etc/nginx/sites-available/default FOR REVERSE PROXY

# server {
#     listen 80;
#     server_name localhost;

#     location / {
#         proxy_pass http://localhost:5000;  # Your backend application
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection 'upgrade';
#         proxy_set_header Host $host;
#         proxy_cache_bypass $http_upgrade;
#     }
# }

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CHANNEL_NAME = 'DougDoug'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
SECRET = os.getenv('SECRET')

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="/etc/ssl/localhost.crt", keyfile="/etc/ssl/localhost.key")  # Paths to your SSL cert and key

clients = set()

async def handle_websocket(websocket):

    clients.add(websocket)

    try:
        async for message in websocket:
            pass
    finally:
        clients.remove(websocket)

async def send_to_clients(event, data):
    if clients:
        message = {
            'event': event,  # Include event name
            'data': data     # Include data associated with the event
        }
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients]) #star is important dont forget the star


esbot = commands.Bot.from_client_credentials(client_id=CLIENT_ID,
                                             client_secret=SECRET)

esclient = eventsub.EventSubClient(esbot,
                                   webhook_secret=SECRET,
                                   callback_route='https://localhost:5000')


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{os.getenv('AUTH_TOKEN')}"), prefix="!", initial_channels=[CHANNEL_NAME])

    async def __ainit__(self):
        try:
            print("initilizing event bot")
            try:
                response = await esclient.subscribe_channel_follows_v2(broadcaster='31507411', moderator="213205254")
                print(f'Response: {response}')
            except Exception as e:
                print(f"Error occurred during subscription: {e}")
            self.loop.create_task(esclient.listen(port=5000))

        except:
            pass

    async def event_message(self, data):

        name = data.author.name
        content = data.content

        message = {
            "name": name,
            "content": content,
            "expiry": 15000
        }
        
        # print(message)
        await send_to_clients('getChat', message)

    
    async def event_ready(self):
        try:
            print(f'Logged in as | {self.nick}', flush=True)

        except Exception as e:
            print(f'Error in event_ready: {e}', flush=True)

@esbot.event()
async def event_eventsub_notification_followV2(payload: eventsub.ChannelFollowData):
    print("received event")
    await send_to_clients('follow', payload.data.user.name)

async def main():
    bot = Bot()
    server = await websockets.serve(handle_websocket, "localhost", 5000, ssl=ssl_context)
    await asyncio.gather(server.wait_closed(), bot.__ainit__()) 

if __name__ == '__main__':
    asyncio.run(main())


