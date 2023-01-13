import json
import requests
import base64

class User:

    def __init__(self, client_credentials):
        auth_header = base64.b64encode(f"{client_credentials['client_id']}:{client_credentials['client_secret']}".encode())

        # Make a request to the Spotify token endpoint to get an access token
        token_response = requests.post('https://accounts.spotify.com/api/token',
                                       headers={
                                            'Authorization': f'Basic {auth_header.decode()}',
                                            'Content-Type': 'application/x-www-form-urlencoded'},
                                        data={'grant_type': 'client_credentials'},
                                        timeout=60)

        # Extract the access token from the response
        self.access_token = token_response.json()['access_token']

        #Example usage
        # playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers={
        #     'Authorization': f'Bearer {access_token}',
        # })


    def get_new_releases_by_continent(continent: str):
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
        pass

    
    def get_users_top_genres(self):
        """Finds the top 5 genres from a user's saved tracks

        Returns
        -------
        List
            A list of the top 5 genres that a user likes

        Examples
        --------
        >>> User.get_users_top_genres()
        """
        pass