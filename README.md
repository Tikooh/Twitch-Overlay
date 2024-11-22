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

