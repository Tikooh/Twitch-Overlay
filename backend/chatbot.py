import websockets
import json
from twitchio.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

clients = set()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class ChatBot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{AUTH_TOKEN}"), prefix="!", initial_channels=["george_f0"])

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


async def handle_websocket(websocket):

    clients.add(websocket)

    try:
        async for message in websocket:
            pass
    finally:
        clients.remove(websocket)

async def send_to_clients(event, data):
    if clients:
        print(clients)
        message = {
            'event': event,  # Include event name
            'data': data     # Include data associated with the event
        }
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients]) #star is important dont forget the star
        
async def main():
    chatbot = ChatBot()
    server = await websockets.serve(handle_websocket, "localhost", 5000)
    await asyncio.gather(server.wait_closed(), chatbot.start()) 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
