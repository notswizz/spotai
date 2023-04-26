import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public')
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_track_uris(track_names, access_token, refresh_token):
    SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope='playlist-modify-public')
                            
    # Refresh the access token if necessary
    token_info = sp_oauth.refresh_access_token(refresh_token)
    access_token = token_info['access_token']

    sp = spotipy.Spotify(auth=access_token)
    # rest of the function

    track_uris = []
    for track_name in track_names:
        try:
            results = sp.search(q=track_name, limit=1, type="track")
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401 and e.msg == "The access token expired":
                new_token_info = sp_oauth.refresh_access_token(refresh_token)
                access_token = new_token_info["access_token"]
                sp.set_auth(access_token)

                results = sp.search(q=track_name, limit=1, type="track")
            else:
                raise e

        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])
        else:
            print(f"No results found for '{track_name}', skipping.")
    return track_uris

def save_playlist_to_spotify(playlist_name, track_uris, access_token):
    auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public')
    sp = spotipy.Spotify(auth_manager=auth_manager, auth=access_token)
    
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, track_uris)

    return playlist['external_urls']['spotify']
