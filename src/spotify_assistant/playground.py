from spotify_assistant import User
import requests, base64, json
from urllib.parse import urlencode
import connector


if __name__ == "__main__":

    # Two ways to get token
    # Either create a dict with two keys "id" and "secret"
    # Pass it in get_access_token()
    # Or create a config.py file here
    # And define variables clientId = ... and clientSecret = ...
    # Remember not to commit the config.py file
    token = connector.get_access_token()
    print(token)

    header = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    new_releases = requests.get("https://api.spotify.com/v1/browse/new-releases?country=US", headers=header, timeout=60).json()
    print(json.dumps(new_releases, indent=4))
