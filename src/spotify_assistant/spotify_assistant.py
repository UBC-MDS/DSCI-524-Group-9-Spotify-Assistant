import json
import requests
from datetime import date
from collections import Counter
from connector import get_no_access_token
import pandas as pd
from collections import defaultdict
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

class User:

    def __init__(self, client_credentials):
        
        scopes = ["playlist-read-private",
                  "playlist-read-collaborative",
                  "playlist-modify-private",
                  "user-library-read"]
        
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_credentials['client_id'],
                client_secret=client_credentials['client_secret'],
                redirect_uri="http://127.0.0.1:8000",
                scope=','.join(scopes)))

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
        saved_tracks = []
        
        offset = 0
        tracks = self.sp.current_user_saved_tracks(limit=None).get('items')
        while tracks != []:
            saved_tracks.extend(tracks)
            offset += len(tracks)
            tracks = self.sp.current_user_saved_tracks(limit=None, 
                                                       offset=offset).get('items')

        for track in saved_tracks:
            for artist in track['track']['artists']:
                artists.add(artist['id'])

        for artist_id in list(artists):
            artist_info = self.sp.artist(artist_id)
            
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
        # check valid playlists argument
        if not (playlists is None or isinstance(playlists, list)):
            raise TypeError('playlists must be a list or None')

        # request a user's playlists
        playlists_output = {}
        user_playlists = requests.get("https://api.spotify.com/v1/me/playlists", headers=self.user_headers, timeout=60).json()

        # create dictionary where each key is a playlist name
        for response in user_playlists['items']:
            if (playlists):
                if response['name'] in playlists:
                    playlists_output[response['name']] = {'id': response['id'], 'songs': []}
                else:
                    continue
            else:
                playlists_output[response['name']] = {'id': response['id'], 'songs': []}
        
        # return empty dictionary if no playlists were added
        if len(playlists_output) == 0:
            print('No playlists were found')
            return playlists_output
        
        # get songs from each playlist
        for playlist in playlists_output:
            playlist_songs = requests.get(f"https://api.spotify.com/v1/playlists/{playlists_output[playlist]['id']}/tracks", headers=self.user_headers, timeout=60).json()
            for song in playlist_songs['items']:
                playlists_output[playlist]['songs'].append(song['track']['name'])

        return playlists_output
        


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
        top_artists = set()
        new_songs = []
        # Get user's top 3 artists with their artist id information
        user_artists = self.sp.current_user_top_tracks(limit=3, time_range='short_term').get('items')
        
        # Assuming within items we have artist name and id as fields
        for response in user_artists['items']:
            top_artists.add(response['id'])
        
        top_artists = list(top_artists)
        
        # Get 5 recommended song uri's
        rec_songs = self.sp.recommendations(seed_artists=top_artists, limit=num_songs).get('items')
        
        for response in rec_songs['tracks']:
            new_songs.append(response['uri'])
        
        # Create a new playlist to put the new songs in
        possible_name = input("Please enter a name for the new playlist: ")
        if playlist_name:
            pass
        else:
            playlist_name = f"{pd.to_datetime('today').date()} Recommended Songs"
            
        new_playlist = self.sp.user_playlist_create(self.sp.current_user()['id'], playlist_name)
        
        playlist_url = new_playlist['external_urls']['spotify']
        playlist_id = new_playlist['id'] 
       
        # Adding recommended songs to playlist
        add_songs = self.sp.playlist_add_items(playlist_id=playlist_id, new_songs)
        
        print(f"Here is a link to the new playlist: {playlist_url}")