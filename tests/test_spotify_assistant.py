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
    cc_map = spotify_assistant.User.get_map()

    # Assert that the map is a dict object
    assert isinstance(cc_map, dict) == True

    # Assert the number of continents to be correct
    assert len(cc_map) == 5

    # Assert the number of countires in Asia to be correct
    assert len(cc_map['Asia']) == 51

    # Assert the number of countires in Europe to be correct
    assert len(cc_map['Europe']) == 51

    # Assert the number of countires  in Americas to be correct
    assert len(cc_map['Americas']) == 57

    # Assert the number of countires in Africa to be correct
    assert len(cc_map['Africa']) == 60

    # Assert the number of countires in Oceania to be correct
    assert len(cc_map['Oceania']) == 29



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

    # Test that all playlists are returned when no filter is added
    allPlaylists = spotify_assistant.User.filter_playlists(fake_playlist_output)
    assert allPlaylists == {
        'night drives': '4k3qVV6kpEPU8BbPNFExGH',
        'boss rush': '2QbimdtcVdsCxocvmIDNgt'
    }

    # Test that function returns proper song names
    songnames = spotify_assistant.User.format_songs(fake_song_output)
    assert songnames == ['False Knight']


def test_get_song_recommendations():
    Random_User = spotify_assistant.User
    artists_info = json.load(open('tests/artist_info.json', 'r'))
        
    example_artist_info = [{
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
    }]
        
        
    # Test that artist id information is correctly extracted
    example_id = Random_User.extract_artist_id(example_artist_info)
    assert example_id == ['6uRJnvQ3f8whVnmeoecv5Z'], "Artist id was not correctly extracted"


    # Test that all of the artist id's were extracted
    many_ids = Random_User.extract_artist_id(artists_info['artists'])
    assert len(many_ids) == 20, "Incorrect number of artist id's extracted"

    # Test that an empty list is returned if there is no artist information
    no_artist = Random_User.extract_artist_id([])
    assert len(no_artist) == 0
    assert isinstance(no_artist, list)
