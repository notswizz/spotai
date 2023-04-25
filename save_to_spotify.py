import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public')
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_track_uris(track_names, access_token):
    sp = spotipy.Spotipy(auth=access_token)
    track_uris = []
    for track_name in track_names:
        results = sp.search(q=track_name, limit=1, type="track")
        track_uris.append(results['tracks']['items'][0]['uri'])
    return track_uris

def save_playlist_to_spotify(playlist_name, track_uris):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description="")
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, track_uris)
    return playlist['external_urls']['spotify']
