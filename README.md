# Twitch-Overlay

## FOR GENERATING AUTH TOKEN FROM CLIENT ID AND SECRET

In your web browser type in the following to get an authorisation code from the url
```
https://id.twitch.tv/oauth2/authorize?response_type=code
&client_id=abc123def456
&redirect_uri=http://localhost:5000
&scope=<Desired-scope>
  ```

Use Curl to exchange your authorisation code for an auth token
```
curl -X POST https://id.twitch.tv/oauth2/token \
-d client_id=<YOUR_CLIENT_ID> \
-d client_secret=<YOUR_CLIENT_SECRET> \
-d code=<AUTHORIZATION_CODE> \
-d grant_type=authorization_code \
-d redirect_uri=<YOUR_REDIRECT_URI>
```

Make sure to set up nginx as a reverse proxy and create a self-signed ssl.

Also set up ngrox as a tunneling service to get a public facing ip

```
server {
    listen 443 ssl;
    server_name fgeorge.org www.fgeorge.org;

    location /.well-known/acme-challenge/ {
    root /var/www/certbot;  # Ensure this points to the correct directory
    }

    ssl_certificate /etc/ssl/localhost.crt;
    ssl_certificate_key /etc/ssl/localhost.key;

    # Enable SSL protocols
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';

    # Redirect HTTP to HTTPS
    location / {
        proxy_pass https://localhost:5000;  # Your TwitchIO server
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Optionally, if you want to redirect all HTTP traffic to HTTPS
server {
    listen 80;
    server_name fgeorge.org www.fgeorge.org;

    location / {
        return 301 https://$host$request_uri;
    }
}
```

I don't know what is going on but:

Eventsub server -> cloudflare reverse proxy ssl -> cloudflare domain (fgeorge.org) -> nginx reverse proxy -> localhost:4000

ensure the firewall does not block

eventsub sends a challenge to domain to ensure it is owned by the user. If this is not properly handled the connection is terminated

```
use curl -I https://www.fgeorge.org/eventsub/ to check if web host is available
````

```
twitch event verify-subscription subscribe -F https://www.fgeorge.org/eventsub/ -s <YOUR WEBHOOK SECRET> for testing eventsub
```

curl -X POST http://fgeorge.org/eventsub/ -d '{"test": "data"}' -H "Content-Type: application/json"
error code: 522

server {
    listen 80;
    server_name fgeorge.org www.fgeorge.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://localhost:4000;  # Your app running locally
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
eventsub_server = await websockets.serve(handle_websocket, "0.0.0.0", 4000)

 Cloudflare:
SSL/TLS encryption
Current encryption mode:

Flexible

	

A
fgeorge.org

Proxied
```

EVENTSUB TAKES HTTP NOT WEBSOCKET IT DOES NOT COMMUNICATE WITH WEBSOCKETS

`websocat wss://fgeorge.org/eventsub/ -t`

`sudo certbot certonly --manual --preferred-challenges dns -d fgeorge.org -d www.fgeorge.org`

`sudo netstat -tuln | grep 80`

`sudo ufw status`

`curl -X POST https://fgeorge.org/eventsub/ -d '{"test": "data"}' -H "Content-Type: application/json"`

```
server {
    listen 443 ssl;
    server_name fgeorge.org www.fgeorge.org;

    ssl_certificate /etc/letsencrypt/live/fgeorge.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fgeorge.org/privkey.pem;

    # Proxy HTTP POST requests
    location /eventsub/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy WebSocket connections
    location /ws/ {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```
sudo nginx -t
sudo systemctl reload nginx
```

Make sure to enable strict mode on cloudflare and disable cloudflare reverse proxy

`sudo ufw allow 8443/tcp`
`curl -X POST https://fgeorge.org:8443/eventsub/ -d '{"test": "data"}' -H "Content-Type: application/json"`

```
curl 127.0.0.1:443
<html>
<head><title>400 The plain HTTP request was sent to HTTPS port</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<center>The plain HTTP request was sent to HTTPS port</center>
<hr><center>nginx/1.22.0 (Ubuntu)</center>
</body>
</html>
```

Enabling port forwarding on router to point external traffic on port 443 to my server on port 443
`https://www.reddit.com/r/VirginMedia/comments/ywwfpf/hub_5_port_forwarding/`

```
curl https://fgeorge.org
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

```
twitch event verify-subscription subscribe -F https://fgeorge.org/eventsub/ -s 976de7c7a56fdb25bdb01403f3025b2e452a
✗ Invalid response. Received <html>
<head><title>502 Bad Gateway</title></head>
<body>
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.22.0 (Ubuntu)</center>
</body>
</html>
 as body, expected 19186602-fa35-963b-9e03-3827af139cf6
✗ Invalid content-type header. Received type text/html. Expecting text/plain.
✗ Invalid status code. Received 502, expected a 2XX status
```

`curl --tlsv1.2 -k -X POST https://127.0.0.1:8443/eventsub/ -d '{"test": "data"}' -H "Content-Type: application/json"` and ensure http has proper ssl_context

force correct protocol

`sudo tail -f /var/log/nginx/error.log`

```
POST /eventsub/ HTTP/1.1", upstream: "http://127.0.0.1:4000/eventsub/", host: "fgeorge.org"
2024/11/25 22:30:54 [error] 95239#95239: *47 upstream prematurely closed connection while reading response header from upstream, client: 94.174.171.208, server: fgeorge.org, request: "POST /eventsub/ HTTP/1.1", upstream: "http://127.0.0.1:4000/eventsub/", host: "fgeorge.org"
```

```
rg, request: "GET /wp-admin/setup-config.php HTTP/1.1", host: "fgeorge.org"
2024/11/25 22:50:08 [error] 102753#102753: *91 open() "/usr/share/nginx/html/wp-admin/setup-config.php" failed (2: No such file or directory), client: 94.174.171.208, server: fgeorge.org, request: "GET /wp-admin/setup-config.php HTTP/1.1", host: "fgeorge.org"
this is someone botting me
^C
```

```
 twitch event verify-subscription subscribe -F https://fgeorge.org/eventsub/ -s 976de7c7a56fdb25bdb01403f3025b2e452a7ef982
✗ Invalid response. Received Errorrrrr as body, expected f7863bb9-f3c3-8211-5474-196f98fde7ff
✔ Valid content-type header. Received type text/plain with charset utf-8
✗ Invalid status code. Received 500, expected a 2XX status

```

```
async def handle_http(request):
    try:
        data = await request.json()
        print({data})
        
        if 'challenge' in data:
            return web.Response(text=data['challenge'], content_type='text/plain', status=200)
        
        return web.Response(text='Invalid Data', status=400)

    except Exception:
        print({Exception})
        return web.Response(text="Errorrrrr", content_type='text/plain', status=500)
```

```
twitch event verify-subscription subscribe -F https://fgeorge.org/eventsub/ -s 976de7c7a56fdb25bdb01403f3025b2e452a7ef9825611588478bdfa8dbf4e53
✗ Invalid response. Received 500 Internal Server Error
```

```
async def handle_http(request):
    data = await request.json()
    try:       
        print(data)
        
        if 'challenge' in data:
            return web.Response(text=data['challenge'], content_type='text/plain', status=200)
        
        return web.Response(text='Invalid Data', status=400)

    except Exception:
        print(Exception)
        return web.Response(text="Errorrrrr", content_type='text/plain', status=500)
```
```
{'challenge': '75fd7e74-b3e9-8619-3d71-1fd2fca76986', 'subscription': {'id': '3f1ac488-4812-eb66-3435-cc405140501b', 'status': 'webhook_callback_verification_pending', 'type': 'channel.subscribe', 'version': '1', 'condition': {'broadcaster_user_id': '38726782'}, 'transport': {'method': 'webhook', 'callback': 'https://fgeorge.org/eventsub/'}, 'created_at': '2024-11-25T23:17:12.884272245Z', 'cost': 0}}
INFO:aiohttp.access:127.0.0.1 [25/Nov/2024:23:17:12 +0000] "POST /eventsub/ HTTP/1.0" 200 189 "-" "twitch-cli/1.1.24"
```
```
twitch event verify-subscription subscribe -F https://fgeorge.org/eventsub/ -s 976de7c7a56fdb25bdb01403f3025b2e452a7ef9825611588478bdfa8dbf4e53
✔ Valid response. Received challenge 75fd7e74-b3e9-8619-3d71-1fd2fca76986 in body
✔ Valid content-type header. Received type text/plain with charset utf-8
✔ Valid status code. Received status 200
```