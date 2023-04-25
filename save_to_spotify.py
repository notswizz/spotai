import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Using the environment variable names you've provided
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('SECRET_ID')
REDIRECT_URI = os.environ.get('KEY')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-public"))

def save_playlist_to_spotify(user_id, playlist_name, track_uris):
    new_playlist = sp.user_playlist_create(user_id, playlist_name)
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], track_uris)

    return new_playlist["external_urls"]["spotify"]

