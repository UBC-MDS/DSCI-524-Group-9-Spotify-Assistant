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
                  "user-library-read",
                  "user-top-read",
                  "playlist-modify-private",
                  "playlist-modify-public"]
        
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_credentials['client_id'],
                client_secret=client_credentials['client_secret'],
                redirect_uri="http://127.0.0.1:8000",
                scope=','.join(scopes)))
        
    def __get_releases(self, continent: str, limit: int = 5):
        """Gets the top new releases

        Parameters
        -------
        continent: str
            The continent where the new releases were published
        limit: int
            Number of new releases to return
            
        Returns
        -------
        List
            A list of dictionaries. Each dictionary contains metadata of 1 new release.
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

        all_releases = []
        
        for country_code in cc_map[continent]:
            try: 
                new_releases = self.sp.new_releases(country_code)
                all_releases.append(new_releases)
            except: 
                continue
        
        return all_releases
    
    def extract_albums(self, all_releases):
        """Extracts the album names and the corresponding artists

        Parameters
        -------
        all_releases: list
            A list of dictionaries. Each dictionary contains metadata for 1 new release.
            
        Returns
        -------
        List
            A list of dictionaries. Each dictionary contains metadata for 1 new release.
        """
        data = []
        for new_releases in all_releases:
            for item in new_releases['albums']['items']:
                album_name = item['name']
                artist_list = [x['name'] for x in item['artists']]
                data.append("{}, produced by {}".format(album_name, ",".join(artist_list)))
        
        return data

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

        all_releases = self.__get_releases(continent, limit)
        
        albums = self.extract_albums(all_releases)

        return albums[:limit]

        
    def __get_saved_track(self):
        """Returns the user's saved tracks

        Returns
        -------
        List
            A list of dictionaries. Each dictionary contains metadata of 1 track.
        """
        saved_tracks = []
        offset = 0
        
        tracks = self.sp.current_user_saved_tracks(limit=None).get('items')
        while tracks != []:
            saved_tracks.extend(tracks)
            offset += len(tracks)
            tracks = self.sp.current_user_saved_tracks(limit=None, 
                                                       offset=offset).get('items')
            
        return saved_tracks
    
    def __get_artists(self, artists):
        """Returns the metadata of a list of artists

        Parameters
        ----------
        artists : list
            list of artist IDs (strings)
            
        Returns
        -------
        List
            A list of dictionaries. Each dictionary contains metadata of 1 artist.
        """
        artist_information = []
        
        for artist_id in list(artists):
            artist_information.append(self.sp.artist(artist_id))
        
        return artist_information
    
    @classmethod
    def get_top_genres(cls, artist_information):
        """Returns the most commonly occuring genres among different artists
        
        Parameters
        ----------
        artist_information : list
            list of dictionaries containing artist metadata
            
        Returns
        -------
        List
            A list of most common genres
        """
        genre_count = Counter()
        
        for artist_info in artist_information:
            if 'genres' in artist_info:
                for genre in artist_info['genres']:
                    genre_count[genre] += 1
        
        genres = [genre[0] for genre in genre_count.most_common(5)]
        
        return genres
    
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
        artists = set()
        
        # Get user's saved tracks
        saved_tracks = self.__get_saved_track()
        
        for track in saved_tracks:
            for artist in track['track']['artists']:
                artists.add(artist['id'])

        # Get information on all artists
        artist_information = self.__get_artists(artists)
        
        #The driver function 
        genres = self.get_top_genres(artist_information)
        
        return genres

    def __get_all_playlists(self):
        """Calls the spotify api and returns the current user's saved/owned playlists
        
        Returns
        -------
        list
            A list of spotify responses containing information about a user's playlists
        """
        all_playlists = []
        offset = 0
        user_playlists = self.sp.current_user_playlists(limit=None).get('items')
        while user_playlists != []:
            all_playlists.extend(user_playlists)
            offset += len(user_playlists)
            user_playlists = self.sp.current_user_playlists(limit=None, offset=offset).get('items')
        return all_playlists
    
    @classmethod
    def filter_playlists(cls, playlist_response, playlists = None):
        """Filters a spotify playlist response for specified playlists

        Parameters
        ----------
        playlist_response : list
            list of spotify responses containing information about playlists
        playlists : list
            list of playlist names (strings) to get songs from, defaults to all

        Returns
        -------
        dict
            A dictionary with the names of playlists as keys,
            and the playlist id as the value
        """
        # check valid playlists argument
        if not (playlists is None or isinstance(playlists, list)):
            raise TypeError('playlists must be a list or None')
        
        filtered_playlists = {}

        # create dictionary where each key is a playlist name
        for response in playlist_response:
            if (playlists):
                if response['name'] in playlists:
                    filtered_playlists[response['name']] = response['id']
                else:
                    continue
            else:
                filtered_playlists[response['name']] = response['id']
        
        return filtered_playlists

    def __get_one_playlists_songs(self, playlist_id):
        """Calls the spotify api and returns the all the songs in a playlist
        
        Returns
        -------
        list
            A list of spotify responses containing all the songs in a playlist
        """
        all_songs = []
        offset=0
        playlist_songs = self.sp.playlist_items(playlist_id=playlist_id, limit=None).get('items')

        while playlist_songs != []:
            all_songs.extend(playlist_songs)
            offset += len(playlist_songs)
            playlist_songs = self.sp.playlist_items(
                playlist_id=playlist_id, limit=None, offset=offset
            ).get('items')
        return all_songs
    
    @classmethod
    def format_songs(cls, song_response):
        """Formats a spotify response into just song names

        Parameters
        ----------
        playlist_response : list
            list of spotify responses containing information about playlists
        playlists : list
            list of playlist names (strings) to get songs from, defaults to all

        Returns
        -------
        dict
            A dictionary with the names of playlists as keys,
            and the playlist id as the value
        """
        song_list = []
        for song in song_response:
            song_list.append(song['track']['name'])
        return song_list

    def get_users_playlists_songs(self, playlists = None):
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
        playlists_output = {}
        
        # request a user's playlists
        all_playlists = self.__get_all_playlists()
        filtered_playlists = self.filter_playlists(all_playlists, playlists)
        
        # return empty dictionary if no playlists were added
        if len(filtered_playlists) == 0:
            print('No playlists were found')
            return playlists_output
        
        # get songs from each playlist
        for playlist in filtered_playlists:
            all_songs = self.__get_one_playlists_songs(playlist_id = filtered_playlists[playlist])
            playlists_output[playlist] = self.format_songs(all_songs)
            
        return playlists_output
        


    def get_song_recommendations(self, playlist_name = None, num_songs = 10):
        """Creates a playlist containing recommended songs based on the user's top 3 artists.
        If there are no top artists, use the user's first three saved tracks.

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
        user_artists = self.sp.current_user_top_artists(limit=3, time_range='short_term').get('items')
        
        # Assuming within items we have artist name and id as fields
        if len(user_artists) > 0 :
            for response in user_artists['items']:
                top_artists.add(response['id'])
        
            top_artists = list(top_artists)
            
            # Get 5 recommended song uri's
            rec_songs = self.sp.recommendations(seed_artists=top_artists, limit=num_songs).get('items')
        else:
            rec_songs = self.sp.recommendations(seed_genres=self.sp.recommendation_genre_seeds()['genres'][:5], 
                                                limit=num_songs)

        for track in rec_songs['tracks']:
            new_songs.append(track['uri'])
        
        # return new_songs
        
        # Create a new playlist to put the new songs in
        playlist_name = input("Please enter a name for the new playlist: ")
        if playlist_name:
            pass
        else:
            playlist_name = f"{pd.to_datetime('today').date()} Recommended Songs"
            
        new_playlist = self.sp.user_playlist_create(self.sp.current_user()['id'], playlist_name)
        
        playlist_url = new_playlist['external_urls']['spotify']
        playlist_id = new_playlist['id'] 
       
        # Adding recommended songs to playlist
        add_songs = self.sp.playlist_add_items(playlist_id=playlist_id, items = new_songs)
        
        print(f"Here is a link to the new playlist: {playlist_url}")
