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

message_list = []

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
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients])


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{os.getenv('AUTH_TOKEN')}"), prefix="!", initial_channels=[CHANNEL_NAME])

    async def event_message(self, data):

        global message_list

        name = data.author.name
        content = data.content

        message = {
            "name": name,
            "content": content
        }
        
        message_list.append(message)
        print(message_list)
        await send_to_clients('getChat', message_list[-10:])

        # await self.handle_commands(message)
    
    async def event_ready(self):
        try:
            print(f'Logged in as | {self.nick}', flush=True)
        except Exception as e:
            print(f'Error in event_ready: {e}', flush=True)
    
    async def close(self):
        await super().close()

async def main():
    bot = Bot()
    server = await websockets.serve(handle_websocket, "localhost", 5000)
    await asyncio.gather(server.wait_closed(), bot.start()) 

if __name__ == '__main__':
    asyncio.run(main())


