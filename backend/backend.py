import os
import websockets
from dotenv import load_dotenv
from twitchio.ext import commands, eventsub
import json
import asyncio


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CHANNEL_NAME = 'ohnePixel'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
SECRET = os.getenv('SECRET')

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
        print(clients)
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
            await esclient.subscribe_channel_follows_v2(broadcaster='43683025')

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
        
        print(message)
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
    server = await websockets.serve(handle_websocket, "localhost", 5000)
    await asyncio.gather(server.wait_closed(), bot.start(), bot.__ainit__()) 

if __name__ == '__main__':
    asyncio.run(main())


