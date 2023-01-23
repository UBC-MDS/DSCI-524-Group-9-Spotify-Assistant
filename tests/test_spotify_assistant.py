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
    artists_info = json.load(open('tests/artist_info.json', 'r'))
    RandomUser = spotify_assistant.User

    # Test with invalid continent name
    with pytest.raises(TypeError, match = 'Limit parameter invalid'):
        RandomUser.get_new_releases_by_continent("ContinentThatDoesNotExist")

    # Test with invalid parameter
    with pytest.raises(TypeError, match = 'Continent parameter invalid. Check for typos'):
        RandomUser.get_new_releases_by_continent("Asia", limit=-1)

    # Test if the function returns expected number of outputs
    data = RandomUser.get_new_releases_by_continent("Asia", limit=5)
    assert len(data) == 5

def test_get_playlists_songs():

    # Create fake API call outputs
    fake_playlist_output = [{'collaborative': False,
    'description': 'roof down nighttime speeding down city highways (80s-90s city pop vibes)',
    'name': 'night drives',
    'id': '4k3qVV6kpEPU8BbPNFExGH',
    'type': 'playlist'},
    {'collaborative': False,
    'description': 'battle themes that absolutely slap',
    'id': '2QbimdtcVdsCxocvmIDNgt',
    'name': 'boss rush',
    'type': 'playlist'}]

    fake_song_output = [{'added_at': '2022-05-15T19:06:46Z',
    'track': {'album': {'album_type': 'album',
        'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/13kMpt8IdcHcdxPLcJrgU2'},
        'href': 'https://api.spotify.com/v1/artists/13kMpt8IdcHcdxPLcJrgU2',
        'id': '13kMpt8IdcHcdxPLcJrgU2',
        'name': 'Christopher Larkin',
        'type': 'artist',
        'uri': 'spotify:artist:13kMpt8IdcHcdxPLcJrgU2'}],
        'id': '4XgGOMRY7H4hl6OQi5wb2Z',
        'name': 'Hollow Knight (Original Soundtrack)',
        'type': 'album'},
        'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/13kMpt8IdcHcdxPLcJrgU2'},
        'href': 'https://api.spotify.com/v1/artists/13kMpt8IdcHcdxPLcJrgU2',
        'id': '13kMpt8IdcHcdxPLcJrgU2',
        'name': 'Christopher Larkin',
        'type': 'artist',
        'uri': 'spotify:artist:13kMpt8IdcHcdxPLcJrgU2'}],
        'name': 'False Knight',
        'type': 'track'}}]

    # Test with invalid playlists argument
    with pytest.raises(TypeError, match = 'must be a list or None'):
        spotify_assistant.User.filter_playlists(fake_playlist_output, playlists=2)

    # Test with no playlists matching the list
    noMatch = spotify_assistant.User.filter_playlists(fake_playlist_output, playlists=['aaa'])
    assert isinstance(noMatch, dict)
    assert len(noMatch) == 0

    # Test that matching playlists are returned
    yesMatch = spotify_assistant.User.filter_playlists(fake_playlist_output, playlists=['night drives', 'aaa'])
    assert yesMatch == {'night drives': '4k3qVV6kpEPU8BbPNFExGH'}

    # Test that function returns proper song names
    songnames = spotify_assistant.User.format_songs(fake_song_output)
    assert songnames == ['False Knight']


def test_get_song_recommendations():
    credentials = None
    Random_User = spotify_assistant.User(credentials)

    example_seeds = ['2rRUfv2w535SEUV1YO5SP6', '6uRJnvQ3f8whVnmeoecv5Z']
    example_seed_type = 'artists'

    example_artist_info = {
        'external_urls': {'spotify': 'https://open.spotify.com/artist/6uRJnvQ3f8whVnmeoecv5Z'},
        'followers': {'href': None, 'total': 179579},
        'genres': ['german orchestra', 'orchestra'],
        'href': 'https://api.spotify.com/v1/artists/6uRJnvQ3f8whVnmeoecv5Z',
        'id': '6uRJnvQ3f8whVnmeoecv5Z',
        'images': [
            {'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb92e0a1e423bd8590dcd43bda', 'width': 640},
            {'height': 320, 'url': 'https://i.scdn.co/image/ab6761610000517492e0a1e423bd8590dcd43bda', 'width': 320},
            {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f17892e0a1e423bd8590dcd43bda', 'width': 160}
        ],
        'name': 'Berliner Philharmoniker',
        'popularity': 74,
        'type': 'artist',
        'uri': 'spotify:artist:6uRJnvQ3f8whVnmeoecv5Z'
    }


    # Test that artist id's are correctly extracted
    example_id = Random_User.__extract_artist_id(example_artist_info)
    assert example_id == ['6uRJnvQ3f8whVnmeoecv5Z'], "Artist id was not correctly extracted"


    # Test that the number of recommended songs to generate is between 1 and 100
    with pytest.raises(ValueError, match = 'Number of songs to recommend must be between 1 and 100 (inclusive)'):
        Random_User.__get_recommended_songs(example_seed_type, example_seeds, num_songs=123)

    # Test that new songs were generated, and that the correct number of songs was generated
    recommended_songs = Random_User.__get_recommended_songs(example_seed_type, example_seeds, 10)
    assert len(recommended_songs) > 0, "New songs were not generated. Check the input seeds."
    assert len(recommended_songs) == 10, "Incorrect number of songs generated."
