from flask import Flask, jsonify, request
import os
from flask_cors import CORS
from dotenv import load_dotenv
from twitchio.ext import commands
import threading
import asyncio
import json

import logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CHANNEL_NAME = 'george_f0'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

message_list = []


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{os.getenv('AUTH_TOKEN')}"), prefix="!", initial_channels=[CHANNEL_NAME])

    async def event_message(self, message):

        global message_list

        name = message.author.name
        content = message.content

        message = {
            "name": name,
            "content": content
        }
        
        message_list.append(message)

        message_list = message_list[-5:]
    
    async def event_ready(self):
        try:
            print(f'Logged in as | {bot.nick}', flush=True)
        except Exception as e:
            print(f'Error in event_ready: {e}', flush=True)



@app.route("/getChat", methods=['GET'])
def get_chat_messages():
    return jsonify(message_list)

def run_app():
    app.run(port=5000)

if __name__ == '__main__':

    bot = Bot()
    flask_thread = threading.Thread(target=run_app)
    flask_thread.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())



