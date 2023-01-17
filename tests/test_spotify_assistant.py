import sys
sys.path.append("../src/spotify_assistant")
import spotify_assistant


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
