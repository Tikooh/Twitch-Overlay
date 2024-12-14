
from './websocket.py' import await
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

bot = commands.Bot(token=(f"oauth:{AUTH_TOKEN}"), prefix="!", initial_channels=["george_f0"])

@bot.event()
async def event_message(data):
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
    
if __name__ == '__main__':
    bot.run()

