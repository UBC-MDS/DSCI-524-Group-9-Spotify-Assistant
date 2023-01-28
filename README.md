# spotify_assistant

A Python package that enriches spotify users' music experience by allowing them to explore their listening trends via REST APIs implemented for Spotify developers.

There is one similar Python package, [Spotipy](https://github.com/spotipy-dev/spotipy) that provides wrapper functions in Python for the Spotify API. This package contains a function for each possible API request, but does not combine any of these requests. Our aim is to create functions that combine multiple requests and provide additional insights for Spotify users.

## Authors
- Caroline Tang
- Chester Wang
- Jenit Jain
- Julie Song

This package was originally created as part of the requirements of DSCI524 (Collaborative Software Development), a course in the Master of Data Science program at the University of British Columbia. All original members of this project abided by the [Code of Conduct](CONDUCT.md).

## Installation

```bash
$ pip install spotify_assistant
```

## Usage

```bash
import spotify_assistant

credentials = {clientId:'xxxxxxxxxxxx', clientSecret: 'xxxxxxxxxxxx'}
RandomUser = User(credentials)
RandomUser.get_song_recommendations("Recommended Songs")
RandomUser.get_users_playlists_songs()
RandomUser.get_users_top_genres()
spotify_assistant.User.get_new_releases_by_continent("Asia")

```

## Functions

- `get_users_top_genres()`: Returns the top 5 genres of music that a user listens to and has saved in the "Your Music" library.
- `get_song_recommendations(playlist_name, num_songs)`: Creates a playlist of recommended songs based on user’s top 3 artists.
- `get_playlists_songs(playlists)`: Returns the songs saved in all the playlists, which are passed as a list to the function.
- `get_new_releases_by_continent(continent, limit)`: Returns the new releases by continent

## Contributing

Interested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

`spotify_assistant` was created by Caroline Tang, Julie Song, Jenit Jain, Chester Wang. It is licensed under the terms of the MIT license.

## Credits

`spotify_assistant` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
