from spotify_assistant import User
import requests, base64, json
from urllib.parse import urlencode
import connector
import pandas as pd
from collections import defaultdict



if __name__ == "__main__":

    # Two ways to get token
    # Either create a dict with two keys "id" and "secret"
    # Pass it in get_access_token()
    # Or create a config.py file here
    # And define variables clientId = ... and clientSecret = ...
    # Remember not to commit the config.py file

    # So Either: token = connector.get_access_token() # With config.py available locally
    # Or:        credentials = {'client_id': "...", 'client_secret': "..."}
    #            token = connector.get_access_token(credentials)

    credentials = {'client_id': "74652d1e1b664c34bacea50da044afc2", 'client_secret': "a76de7b1d254428e8200ea9c74ad3b77"}
    RandomUser = User(credentials)
    RandomUser.get_new_releases_by_continent("Asia")
