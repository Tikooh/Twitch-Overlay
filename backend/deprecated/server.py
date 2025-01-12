import websockets
from websockets.asyncio.server import serve
import json
import asyncio

clients = set()
active_users = []

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
    await asyncio.gather(server.wait_closed())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    