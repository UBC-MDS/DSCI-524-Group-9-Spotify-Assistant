import webbrowser
import base64
import requests
try:
    import config
except:
    print("-- WARNING: Config.py file not found. Pass in a dict with id and secret instead.")

from urllib.parse import urlencode

def get_access_token(client_credentials):
    #The scopes that we require to implement all the functions
    scopes = ["playlist-read-private",
                "playlist-read-collaborative",
                "playlist-modify-private",
                "user-library-read"]

    auth_headers = {
        "client_id": client_credentials['client_id'],
        "response_type": "code",
        "redirect_uri": "http://127.0.0.1:8000",
        "scope": ",".join(scopes)
    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

    #Authorization code you receive that includes rights to the scopes mentioned above
    code = input("Please input code from the authentication URL: ")

    encoded_credentials = base64.b64encode(client_credentials['client_id'].encode() + \
                                           b':' + client_credentials['client_secret'].encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000"
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers, timeout=60)
    token = r.json()['access_token']
    return token


def get_no_access_token(client_credentials=None):
    #The scopes that we require to implement all the functions
    scopes = ["playlist-read-private",
                "playlist-read-collaborative",
                "playlist-modify-private",
                "user-library-read"]

    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    if(client_credentials): message = f"{client_credentials['client_id']}:{client_credentials['client_secret']}"
    else: message = f"{config.clientId}:{config.clientSecret}"

    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data, timeout=60)
    token = r.json()['access_token']
    return token
