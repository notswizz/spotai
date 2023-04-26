import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, render_template, redirect, url_for, session
from generate_playlist import generate_playlist
from save_to_spotify import save_playlist_to_spotify, get_track_uris

app = Flask(__name__)

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public')
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route("/login")
def login():
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = auth_manager.get_access_token(code, as_dict=True)
    session["access_token"] = token_info["access_token"]
    session["refresh_token"] = token_info["refresh_token"]
    return redirect(url_for("index"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if "access_token" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        user_input = request.form['prompt']
        track_names = generate_playlist(user_input)
        if track_names:
            track_uris = get_track_uris(track_names, session["access_token"])
            playlist_url = save_playlist_to_spotify(user_input, track_uris, session["access_token"])  # Include the access token
            return render_template('result.html', playlist_url=playlist_url)
        else:
            error = "Unable to generate a playlist. Please try again."
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route('/result')
def result():
    playlist_url = request.args.get('playlist_url', None)
    return render_template("result.html", playlist_url=playlist_url)

if __name__ == '__main__':
    app.run(debug=True)
