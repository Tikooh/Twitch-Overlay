from flask import Flask, jsonify, request
import os
from flask_cors import CORS
from dotenv import load_dotenv
from twitchio.ext import commands
import threading
import json

import logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CHANNEL_NAME = 'george_f0'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

bot = commands.Bot(
    token=(f"oauth:{os.getenv('AUTH_TOKEN')}"),
    prefix='!',
    initial_channels=[CHANNEL_NAME]
)

message_list = []

@bot.event
async def event_ready():
    try:
        print(f'Logged in as | {bot.nick}', flush=True)
    except Exception as e:
        print(f'Error in event_ready: {e}', flush=True)

@bot.event
async def event_message(message):
    await bot.process_commands(message)

    name = message.author.name
    content = message.content

    message = {
        "name": name,
        "content": content
    }
    
    message_list.append(message)

    message_list = message_list[-5:]

@app.route("/getChat", methods=['GET'])
def get_chat_messages():
    return json.dump(message_list)

def run_bot():
    bot.run()
def run_app():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    run_bot()
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    

    app_thread = threading.Thread(target=run_app)
    app_thread.start()



