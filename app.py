import os
from flask import Flask, render_template, request, redirect, url_for
from generate_playlist import generate_playlist
from save_to_spotify import sp, save_playlist_to_spotify, get_track_uris

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        track_names = generate_playlist(prompt)
        track_uris = get_track_uris(track_names)  # Get track URIs
        user_id = sp.me()["id"]  # Get user id
        spotify_url = save_playlist_to_spotify(user_id, prompt, track_uris)  # Pass user_id and track_uris
        return redirect(url_for('result', spotify_url=spotify_url))

    return render_template('index.html')

@app.route('/result')
def result():
    spotify_url = request.args.get('spotify_url', '')
    return render_template('result.html', spotify_url=spotify_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
