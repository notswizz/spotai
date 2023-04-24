import spotipy
from spotipy.oauth2 import SpotifyOAuth

def save_playlist_to_spotify(playlist_name, track_list):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="4a6221cb520a4097a6d0978642daa986",
                                                   client_secret="9895ce77e9564279878d4eb38c7987c8",
                                                   redirect_uri="http://localhost:8000/callback/",
                                                   scope="playlist-modify-public"))

    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, playlist_name)
    playlist_id = playlist["id"]

    track_ids = []

    for track in track_list:
        if not track.strip():
            continue
        search_result = sp.search(track, type="track", limit=1)
        if search_result["tracks"]["items"]:
            for item in search_result["tracks"]["items"]:
                if "karaoke" not in item["name"].lower() and "instrumental" not in item["name"].lower():
                    track_id = item["id"]
                    track_ids.append(track_id)
                    break

    sp.playlist_add_items(playlist_id, track_ids)
    return playlist["external_urls"]["spotify"]
