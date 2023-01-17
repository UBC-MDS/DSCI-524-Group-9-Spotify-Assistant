import json
import requests
from datetime import date
from collections import Counter
from connector import get_access_token, get_no_access_token
import pandas as pd
from collections import defaultdict


class User:

    def __init__(self, client_credentials=None):

        access_token = get_access_token(client_credentials=client_credentials)
        no_access_token = get_no_access_token(client_credentials=client_credentials)

        self.user_headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        self.user_headers_no_access = {
            "Authorization": "Bearer " + no_access_token,
            "Content-Type": "application/json"
        }

        #Example usage
        # playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers=self.user_headers)


    def get_new_releases_by_continent(self, continent: str, limit: int = 5):
        """Gets the new releases by continent

        Usually the style of music from the same continent are similar,
        and this helps users find and explore songs similar to their taste.

        Parameters
        ----------
        continent : str
            continent name (i.e. Asia, Europe, Oceania, Americas, Africa)

        Returns
        -------
        List
            A list of titles of new releases in String from the corresponding continent

        Examples
        --------
        >>> User.get_new_releases_by_continent("Asia")
        """

        df = pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
        cc_map = defaultdict(list)
        df = df.reset_index()  # make sure indexes pair with number of rows

        for index, row in df.iterrows():
            if(row['alpha-2'] == 'AQ'): continue
            cc_map[row['region']].append(row['alpha-2'])

        assert limit > 0
        assert continent in cc_map

        print("-- Loading new releases in {}, this may take a while...".format(continent))

        data = []
        for country_code in cc_map[continent]:

            url = "https://api.spotify.com/v1/browse/new-releases?country={}".format(country_code)
            r = requests.get(url, headers=self.user_headers_no_access, timeout=60)

            if(r.status_code != 200): continue # Skipping some countries that cannot use spotify

            new_releases = r.json()
            for item in new_releases['albums']['items']:
                album_name = item['name']
                artist_list = [x['name'] for x in item['artists']]
                data.append("{}, produced by {}".format(album_name, ",".join(artist_list)))

        return data[:limit]



    def get_users_top_genres(self):
        """Finds the top 5 genres from a user's saved tracks

        Returns
        -------
        List
            A list of the top 5 genres that a user likes

        Examples
        --------
        >>> credentials = {}
        >>> RandomUser = User(credentials)
        >>> RandomUser.get_users_top_genres()
        """
        genre_count = Counter()
        artists = set()
        user_tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", headers=self.user_headers, timeout=60).json()

        for track in user_tracks_response['items']:
            for artist in track['track']['artists']:
                artists.add(artist['id'])

        for artist in list(artists):
            artist_info = requests.get(f"https://api.spotify.com/v1/artists/{artist}", headers=self.user_headers, timeout=60).json()
            if 'genres' in artist_info:
                for genre in artist_info['genres']:
                    genre_count[genre] += 1

        genres = [genre[0] for genre in genre_count.most_common(5)]
        return genres

    def get_playlists_songs(self, playlists = None):
        """Gets all of the song titles within a user's owned and followed playlists

        Playlists from which to retrieve songs can be specified by name as a list,
        but by default all songs from all of a user's owned and followed playlists will be retrieved.

        Parameters
        ----------
        playlists : list
            list of playlist names (strings) to get songs from, defaults to all

        Returns
        -------
        dict
            A dictionary with the names of playlists as keys,
            and a list of song titles contained in the playlist as values

        Examples
        --------
        >>> credentials = {}
        >>> Caroline = User(credentials)
        >>> Caroline.get_playlists_songs()
        """
        return None


    def get_song_recommendations(self, playlist_name = None, num_songs = 10):
        """Creates a playlist containing recommended songs based on the user's top 3 artists.

        Prints a url link to the new playlist on Spotify.

        Parameters
        ----------
        playlist_name : str
            The name of the newly created playlist. Defaults to 'Recommended Songs'
            with the current date (i.e. "2023-01-14 Recommended Songs").

        num_songs : int
            The number of songs to recommend.

        Examples
        --------
        >>> credentials = {}
        >>> RandomUser = User(credentials)
        >>> RandomUser.get_song_recommendations("Recommended Songs")
        """
        pass
