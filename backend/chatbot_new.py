
import websockets
from websockets.asyncio.server import serve
import json
import asyncio
from server import send_to_clients, addActiveClients
from twitchio.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

clients = set()
active_users = []

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

bot = commands.Bot(token=(f"oauth:{AUTH_TOKEN}"), prefix="!", initial_channels=["george_f0"])

@bot.event()
async def event_message(data):
    name = data.author.name
    content = data.content
    color = data.author.color
    print(name)
    
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
        await addActiveClients(name)

@bot.event()
async def event_ready():
    try:
        print(f'Logged in as | fgeorge', flush=True)

    except Exception as e:
        print(f'Error in event_ready: {e}', flush=True)


@bot.command(name="sprite")
async def change_sprite(ctx: commands.Context, args: str):
    print("here")
    if args == "male":
        await send_to_clients('changeSprite', (ctx.author.name, 'type_male'))

    elif args == "female":
        await send_to_clients('changeSprite', (ctx.author.name, 'type_female'))


async def handle_websocket(websocket):

    clients.add(websocket)
    print("clients")

    try:
        async for message in websocket:
            pass
    finally:
        clients.remove(websocket)
        active_users.clear()

async def addActiveClients(new_client):
    active_users.append(new_client)
    await send_to_clients('newUser', '')


async def send_to_clients(event, data):
    if clients:
        print(clients)
        message = {
            'event': event,  # Include event name
            'data': data     # Include data associated with the event
        }
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients]) #star is important dont forget the star

async def main():
    server = await websockets.serve(handle_websocket, "0.0.0.0", 5000)
    await asyncio.gather(server.wait_closed(), bot.start())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

