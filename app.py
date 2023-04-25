import os
from flask import Flask, render_template, request
from save_to_spotify import get_track_uris, save_playlist_to_spotify
from generate_playlist import generate_playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        track_names = request.form.getlist('track_names')  # Get list of track names
        playlist_name = request.form['playlist_name']  # Get playlist name
        track_uris = get_track_uris(track_names)  # Get track URIs
        playlist_url = save_playlist_to_spotify(playlist_name, track_uris)  # Create playlist and add tracks
        return render_template('results.html', playlist_url=playlist_url)

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's input from the form
        track_names = request.form.get('track_names')
        playlist_name = request.form.get('playlist_name')

        # Split the user's input into a list of track names
        track_names = track_names.split(',')

        # Generate the playlist and get the Spotify URL
        playlist_url = generate_playlist(track_names, playlist_name)

        # Render the template with the Spotify URL
        return render_template('index.html', playlist_url=playlist_url)
    
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 8080)))