# spotify_assistant

A Python package that enriches spotify users' music experience by allowing them to explore their listening trends via REST APIs implemented for Spotify developers.

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

- TODO

## Functions

- `get_users_top_genres()`: Returns the top 5 genres of music that a user listens to and has saved in the "Your Music" library.
- `create_playlsit()`: Creates a playlist of recommended songs based on user’s top artists.
- `get_playlists_songs(playlists)`: Returns the songs saved in all the playlists, which are passed as a list to the function.
- `get_new_releases_by_continent(continent)`: Returns the new releases by continent

## Contributing

Interested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

`spotify_assistant` was created by Caroline Tang, Julie Song, Jenit Jain, Chester Wang. It is licensed under the terms of the MIT license.

## Credits

`spotify_assistant` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
