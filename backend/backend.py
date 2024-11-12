from flask import Flask, jsonify, request
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv
from twitchio.ext import commands
import asyncio
import threading

app = Flask(__name__)
CORS(app)

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CHANNEL_NAME = 'george_f0'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

bot = commands.Bot(
    token=(f"{os.getenv('AUTH_TOKEN')}"),
    prefix='!',
    initial_channels=[CHANNEL_NAME]
)

message_list = []

@bot.event
async def event_ready():
    print(f'Logged in as | {bot.nick}')

@bot.event
async def event_message(message):
    print(message)
    message_list.append(message)
    

@app.route("/getAuth", methods=['GET'])
def get_auth_tokens():
    return jsonify({'auth_token', AUTH_TOKEN})

@app.route("/getChat", methods=['GET'])
def get_chat_messages():
    return jsonify({'messages', message_list})

def run_bot():
    bot.run()

if __name__ == '__main__':

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    

    app.run(debug=True)


