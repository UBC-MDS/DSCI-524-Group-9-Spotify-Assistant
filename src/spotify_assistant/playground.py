from spotify_assistant import User
import requests, base64, json
from urllib.parse import urlencode
import connector
import pandas as pd
from collections import defaultdict



def get_releases_by_country(country_code, headers):
    assert len(country_code) == 2
    url = "https://api.spotify.com/v1/browse/new-releases?country={}".format(country_code)
    new_releases = requests.get(url, headers=header, timeout=60).json()

    data = []
    for item in new_releases['albums']['items']:
        album_name = item['name']
        artist_list = [x['name'] for x in item['artists']]
        data.append((album_name, artist_list))

    return data


def get_country_continent_dict():
    df = pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
    country_continent = {}

    df = df.reset_index()  # make sure indexes pair with number of rows

    for index, row in df.iterrows():
        if(row['alpha-2'] == 'AQ'): continue
        country_continent[row['alpha-2']] = row['region']

    return country_continent


if __name__ == "__main__":

    # Two ways to get token
    # Either create a dict with two keys "id" and "secret"
    # Pass it in get_access_token()
    # Or create a config.py file here
    # And define variables clientId = ... and clientSecret = ...
    # Remember not to commit the config.py file

    # So Either: token = connector.get_access_token() # With config.py available locally
    # Or:        credentials = {'id': "...", 'secret': "..."}
    #            token = connector.get_access_token(credentials)

    token = connector.get_access_token()
    print(token)

    header = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    cc_map = get_country_continent_dict()

    for country in cc_map:
        tmp_releases = get_releases_by_country(country, header)





    res = defaultdict(list)
