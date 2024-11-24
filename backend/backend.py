import os
import websockets
from dotenv import load_dotenv
from twitchio.ext import commands, eventsub
from aiohttp import web
import json
import asyncio
import logging
import ssl

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CHANNEL_NAME = 'george_f0'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
SECRET = os.getenv('SECRET')

clients = set()

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='/etc/letsencrypt/live/fgeorge.org/fullchain.pem', keyfile='/etc/letsencrypt/live/fgeorge.org/privkey.pem')

async def handle_websocket(websocket):

    clients.add(websocket)

    try:
        async for message in websocket:
            pass
    finally:
        clients.remove(websocket)

async def handle_http(request):
    try:
        data = await request.json()
        print({data})
        
        if 'challenge' in data:
            return web.Response(text=data['challenge'], status=200)
        
        return web.Response(text='OK', status=200)

    except Exception:
        print({Exception})
        return web.Response(text="Errorrrrr",status=500)


async def send_to_clients(event, data):
    if clients:
        message = {
            'event': event,  # Include event name
            'data': data     # Include data associated with the event
        }
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients]) #star is important dont forget the star


esbot = commands.Bot.from_client_credentials(client_id=CLIENT_ID,
                                             client_secret=CLIENT_SECRET)

esclient = eventsub.EventSubClient(esbot,
                                   webhook_secret=SECRET,
                                   callback_route='https://fgeorge.org')


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=(f"oauth:{AUTH_TOKEN}"), prefix="!", initial_channels=[CHANNEL_NAME])

    async def __ainit__(self):
        try:
            print("initilizing event bot")
            try:
                response = await esclient.subscribe_channel_follows_v2(broadcaster='213205254', moderator="213205254")
                print(f'Response: {response}')
            except Exception as e:
                print(f"Error occurred during subscription: {e}")
            self.loop.create_task(esclient.listen(port=8443))

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
        
        # print(message)
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

    app = web.Application()
    app.router.add_post('/eventsub/', handle_http)
    http_runner = web.AppRunner(app)
    await http_runner.setup()
    http_server = web.TCPSite(http_runner, '0.0.0.0', 8443, ssl_context=ssl_context)  # Port for HTTP

    await asyncio.gather(server.wait_closed(), http_server.start(), bot.__ainit__(), bot.start()) 

if __name__ == '__main__':
    asyncio.run(main())


