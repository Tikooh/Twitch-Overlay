import websockets
import json
from twitchio.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

clients = set()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class Emoji:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.url = self.get_image_url()

    def get_image_url(self):
        return f"https://static-cdn.jtvnw.net/emoticons/v2/{self.id}/default/dark/3.0"

def parse_emotes(emote_data, message):
    emote_list = []
    for emote in emote_data.split('/'):
        emote_id, pos = emote.split(':')
        for position in pos.split(','):
            start, end = map(int, position.split('-'))
            emote_name = message[start:end + 1]
        emote_list.append(Emoji(emote_name, emote_id))

    return emote_list

def format_message(emote_object_list, message):
    for word in message.split(' '):
        for emoji in emote_object_list:
            if emoji.name == word:
                message = message.replace(word, f"<img src='{emoji.url}' />")
    return message
        
active_users = []

class ChatBot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{AUTH_TOKEN}"), prefix="!", initial_channels=["george_f0"])

    async def event_message(self, data):
        name = data.author.name
        content = data.content
        color = data.author.color
        
        if data.tags.get('emotes', '') != '':
            print(data.tags)
            emotes = data.tags['emotes']
            emote_list = parse_emotes(emotes, content)
            content = format_message(emote_list, content)
            print(content)


        message = {
            "name": name,
            "content": content,
            "color": color,
            "expiry": 15000
        }
        # print(data.tags)
        # print(message)
        await send_to_clients('getChat', message)

        if not (name in active_users):
            active_users.append(name)
            await send_to_clients('newUser', message)
    
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
        active_users.clear()

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
    server = await websockets.serve(handle_websocket, "0.0.0.0", 5000)
    await asyncio.gather(server.wait_closed(), chatbot.start()) 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
