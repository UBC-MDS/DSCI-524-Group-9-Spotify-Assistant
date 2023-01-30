# read version from installed package
from importlib.metadata import version
from . import User
__version__ = version("spotify_assistant")
