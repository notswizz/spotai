import os
from flask import Flask, render_template, request
from save_to_spotify import get_track_uris, save_playlist_to_spotify
from generate_playlist import generate_playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's input from the form
        prompt = request.form.get('prompt')
        playlist_name = request.form.get('playlist_name')

        # Generate the list of song names based on the prompt
        track_names = generate_playlist(prompt)

        # Get the Spotify URIs for the song names
        track_uris = get_track_uris(track_names)

        # Save the playlist to Spotify and get the Spotify URL
        playlist_url = save_playlist_to_spotify(playlist_name, track_uris)

        # Render the template with the Spotify URL
        return render_template('index.html', playlist_url=playlist_url)
    
    # If the request method is not POST, render the empty form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 8080)))
