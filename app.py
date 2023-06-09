import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, render_template, redirect, url_for, session
from generate_playlist import generate_playlist
from save_to_spotify import save_playlist_to_spotify, get_track_uris, set_playlist_image
from generate_image import generate_image_url

app = Flask(__name__)

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public')

def refresh_token_if_needed():
    sp = spotipy.Spotify(auth=session["access_token"])
    try:
        sp.me()
    except spotipy.SpotifyException:
        new_token = auth_manager.refresh_access_token(session["refresh_token"])
        session["access_token"] = new_token["access_token"]
        sp = spotipy.Spotify(auth=session["access_token"])
    return sp

@app.route("/login")
def login():
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = auth_manager.get_access_token(code)
    access_token = token_info["access_token"]
    refresh_token = token_info["refresh_token"]
    session["access_token"] = access_token
    session["refresh_token"] = refresh_token
    return redirect(url_for("index"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if "access_token" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        user_input = request.form['prompt']
        track_names = generate_playlist(user_input)
        if track_names:
            sp = refresh_token_if_needed()
            track_uris = get_track_uris(track_names, session["access_token"], session["refresh_token"])
            playlist_url = save_playlist_to_spotify(user_input, track_uris, session["access_token"])
            image_url = generate_image_url(user_input)

            # Extract playlist_id from the playlist_url
            playlist_id = playlist_url.split('/')[-1].replace('embed/playlist/', '')

            # Set the playlist image
            set_playlist_image(playlist_id, image_url, session["access_token"])

            return render_template('result.html', playlist_url=playlist_url, image_url=image_url, prompt=user_input)

        else:
            error = "Unable to generate a playlist. Please try again."
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
