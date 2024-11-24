from aiohttp import web

async def handle_http(request):
    print("Received request")
    data = await request.json()
    print("Data:", data)
    return web.Response(text="Received data", status=200)

app = web.Application()
app.router.add_post('/eventsub/', handle_http)

if __name__ == '__main__':
    web.run_app(app, port=8443)