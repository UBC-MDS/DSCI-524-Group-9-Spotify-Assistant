from spotify_assistant import spotify_assistant
import pytest
import json

def test_get_users_top_genres():
    artists_info = json.load(open('tests/artist_info.json', 'r'))
    RandomUser = spotify_assistant.User
    
    # Test the number of genres returned
    genres = RandomUser.get_top_genres(artists_info['artists']) 
    assert len(genres) == 5, "Incorrect number of genres returned"
    
    # Test with no artist information
    genres = RandomUser.get_top_genres([]) 
    assert isinstance(genres, list)
    assert len(genres) == 0
    
    # Test with incorrect datatype of the input
    try:
        RandomUser.get_top_genres(artists_info['artists'][0]) 
    except Exception as e:
        assert isinstance(e, Exception)

def test_get_new_releases_by_continent():

    # Create a new user
    credentials = None
    RandomUser = spotify_assistant.User(credentials)

    # Test with invalid continent name
    try:
        RandomUser.get_new_releases_by_continent("ContinentThatDoesNotExist")
    except Exception as e:
        assert isinstance(e, Exception)

    # Test with invalid parameter
    try:
        RandomUser.get_new_releases_by_continent("Asia", limit=-1)
    except Exception as e:
        assert isinstance(e, Exception)

    # Test if the function returns expected number of outputs
    data = RandomUser.get_new_releases_by_continent("Asia", limit=5)
    assert len(data) == 5

def test_get_playlists_songs():
    credentials = None
    testUser = spotify_assistant.User(credentials)

    # Test with invalid playlists argument
    with pytest.raises(TypeError, match = 'must be a list or None'):
        testUser.get_playlists_songs(playlists=2)

    # Test with no playlists matching the list
    noMatch = testUser.get_playlists_songs(playlists=['aaa'])
    assert isinstance(noMatch, dict)
    assert len(noMatch) == 0

    # Test that function returns proper
    yesMatch = testUser.get_playlists_songs(playlists=None)
    assert isinstance(yesMatch, dict)
    assert len(yesMatch) >= 1
