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