import websockets
from websockets.asyncio.server import serve
import json
import asyncio

clients = set()
active_users = []

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
    async with serve(handle_websocket, "0.0.0.0", 5000) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
    