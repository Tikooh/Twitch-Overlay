import os
import websockets
from dotenv import load_dotenv
from twitchio.ext import commands, eventsub
import json
import asyncio


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CHANNEL_NAME = 'george_f0'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
SECRET = ''

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


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{os.getenv('AUTH_TOKEN')}"), prefix="!", initial_channels=[CHANNEL_NAME])

        self.eventsub_client = eventsub.EventSubClient(
            client = self,
            webhook_secret = SECRET,
            callback_route='',
            token=(f"oauth:{os.getenv('AUTH_TOKEN')}")
        )

        user_id = '213205254'


    async def subscribe_to_events(self):
        await self.eventsub_client.subscribe_websocket(
            event_type = "channel.follow",
            condition={"broadcaster_user_id": self.user_id}
        )

    async def on_follow(self, event: eventsub.ChannelFollowData):
        await send_to_clients('follow', {event.user_name})

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

            await self.eventsub_client.listen_websocket()

            await self.subscribe_to_events(self.user_id)

        except Exception as e:
            print(f'Error in event_ready: {e}', flush=True)

async def main():
    bot = Bot()
    server = await websockets.serve(handle_websocket, "localhost", 5000)
    await asyncio.gather(server.wait_closed(), bot.start()) 

if __name__ == '__main__':
    asyncio.run(main())


