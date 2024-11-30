import asyncio
import ssl
from aiohttp import web

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='/home/george/keys/fullchain.pem', keyfile='/home/george/keys/privkey.pem')

async def main():

    app = web.Application()
    http_runner = web.AppRunner(app)
    await http_runner.setup()
    http_server = web.TCPSite(http_runner, '0.0.0.0', 8443, ssl_context=ssl_context)  # Port for HTTP

    await http_server.start()
    await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())