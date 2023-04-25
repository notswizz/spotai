import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


redirect_uri = "https://spotai.herokuapp.com/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['CLIENT_ID'],
                                               client_secret=os.environ['SECRET_ID'],
                                               redirect_uri=redirect_uri,
                                               scope="playlist-modify-public"))

def save_playlist_to_spotify(prompt, playlist):
    user_id = sp.current_user()["id"]
    playlist_name = f"{prompt} playlist"
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=f"Generated by SpotAI for prompt: {prompt}")
    playlist_id = new_playlist["id"]
    
    # Add tracks to the playlist
    sp.user_playlist_add_tracks(user_id, playlist_id, playlist)

    return new_playlist["external_urls"]["spotify"]
