import sys
sys.path.append("../src/spotify_assistant")
import spotify_assistant
import pytest


def test_get_new_releases_by_continent():

    # Create a new user
    credentials = {'client_id': "74652d1e1b664c34bacea50da044afc2", 'client_secret': "a76de7b1d254428e8200ea9c74ad3b77"}
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
        User.filter_playlists(fake_playlist_output, playlists=2)

    # Test with no playlists matching the list
    noMatch = User.filter_playlists(fake_playlist_output, playlists=['aaa'])
    assert isinstance(noMatch, dict)
    assert len(noMatch) == 0

    # Test that matching playlists are returned
    yesMatch = User.filter_playlists(fake_playlist_output, playlists=['night drives', 'aaa'])
    assert yesMatch == {'night drives': '4k3qVV6kpEPU8BbPNFExGH'}

    # Test that function returns proper song names
    songnames = User.format_songs(fake_song_output)
    assert songnames == ['False Knight']
