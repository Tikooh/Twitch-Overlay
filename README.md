# Fgeorge Twitch Bot

`https://twitchio.dev/en/stable/exts/eventsub.html#twitchio.ext.eventsub.ChannelCheerData`

# Authorising Eventsub 

Authorising Eventsub for Twitch differs depending on if you choose to use websockets or webhooks. For webhooks, see `https://dev.twitch.tv/docs/eventsub/handling-webhook-events/` and for websockets see `https://dev.twitch.tv/docs/eventsub/handling-websocket-events/`.

- Webhooks requires an app access token to authenticate
- Websockets require a user access token to authenticate
- Both webhooks and websockets require ssl connection and a public-facing ip


## Setting up Domain

For the public-facing ip I used my domain fgeorge.org registered on Cloudflare. Go to the DNS section and add:
```
A record
name: @ (root)
content: <your public ip> 
Reverse proxy: disabled
```
A records map your domain to your hosting server's ip address.

Enable `Full (Strict)` to enable end-to-end encryption and enforce validation


## Creating SSL Certificate for Domain

to create an ssl certificate for your domain you cannot self-sign because it will not be accepted by Twitch. Use openssl to generate an ssl cert.

Pip install openssl `sudo apt install openssl`

Run `sudo certbot certonly --manual --preferred-challenges dns -d fgeorge.org -d www.fgeorge.org` as you do not want to open your port at the moment to avoid compromising your system

Add a TXT record to your domain
```
name: _acme_challenge
content <provided key>
```

The priv key is stored at `/etc/letsencrypt/live/<domain>`


## Setting up HTTPS Server

When you send a post request to Twitch Eventsub server it will return a challenge, which you must respond with to complete the handshake. If successful a connection will be made. Twitch will send ping to your server which must respond with pong to maintain the connection.

```
async def handle_http(request):
    data = await request.json()
    try:       
        if 'challenge' in data:
            return web.Response(text=data['challenge'], content_type='text/plain', status=200)
        
        return web.Response(text='Invalid Data', status=400)

    except Exception:
        print(Exception)
        return web.Response(text="Error", content_type='text/plain', status=500)
```

You can verify if the server is listening on the port with `sudo netstat -tuln | grep <port>`


## Setting up Nginx for Reverse Proxy

Nginx is required to act as a reverse proxy between your domain and your server host. This is used to redirect traffic from your domain to the correct port of your server.

Install Nginx `sudo apt install nginx`

Start Nginx with `sudo systemctl start nginx`

Edit `/etc/nginx/sites-enabled/default` with

```
server {
    listen 443 ssl; # listens on port 443 for secure connection
    server_name fgeorge.org www.fgeorge.org;

    ssl_certificate /etc/letsencrypt/live/fgeorge.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fgeorge.org/privkey.pem;

    # Proxy HTTP POST requests
    location /eventsub/ {
        proxy_pass http://localhost:4000;
        proxy_set_header Host $host; # host server
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # forwards initial client's ip address to server
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```

Restart nginx with `systemctl reload nginx`

Use `sudo netstat -tuln | grep nginx` to verify ports which nginx is listening on


## Opening your port and removing firewall restriction

You are required to enable port forwarding on your router. This ensures that all traffic labelled under a specified port is forwarded to your device on x port.

Open port 443 on your machine.

Check firewall status with `sudo ufw status` and enable with `sudo ufw allow 443/tcp`


## Generating OAuth Token

Twitch Eventsub requires user access token to authenticate bots.

### Webhooks
You can make a post request containing your client id and secret to get a client credentials token. This is useful for webhooks
```
res = requests.post("https://id.twitch.tv/oauth2/token", data= {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
```

Example in code

```
    res = requests.post("https://id.twitch.tv/oauth2/token", data= {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })

    if res.status_code == 200:
        body = res.json()
        if body["token_type"] != "bearer":
            raise Exception(f"Did not receive correct token type")
        valid_until = datetime.datetime.now() + datetime.timedelta(seconds=body["expires_in"])
        return Auth(body["access_token"], valid_until)
```


### Websockets
Use in either a script or in browser to generate a code which can be exchanged for a user access token

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

Exchange it for a user access token


## Testing eventsub

You will need to add a post to your http server under `/eventsub`

Use `curl --tlsv1.2 -k -X POST https://127.0.0.1:8443/eventsub/ -d '{"test": "data"}' -H "Content-Type: application/json"` to test your localhost

`--tlsv1.2` flag is used to ensure that curl is using correct ssl protocol

Next, you can use twitch event to directly test a subscription event.

Install twitch event using `brew`

```
twitch event verify-subscription subscribe -F https://fgeorge.org/eventsub/ -s <secret>
✔ Valid response. Received challenge 75fd7e74-b3e9-8619-3d71-1fd2fca76986 in body
✔ Valid content-type header. Received type text/plain with charset utf-8
✔ Valid status code. Received status 200
```

## Subscriptions

https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channelfollow


Subscriptions are initially JSON so must be parsed into an object before using. This depends on your language.


The format of a channel follow subscription is as follows:

```
{
    "type": "channel.follow",
    "version": "2",
    "condition": {
        "broadcaster_user_id": "1337",
        "moderator_user_id": "1337"
    },
    "transport": {
        "method": "webhook",
        "secret": "s3cRe7"
    }
}
