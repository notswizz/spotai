import os
from flask import Flask, render_template, request, redirect, url_for
from generate_playlist import generate_playlist
from save_to_spotify import save_playlist_to_spotify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        playlist = generate_playlist(prompt)
        spotify_url = save_playlist_to_spotify(prompt, playlist)
        return redirect(url_for('result', spotify_url=spotify_url))

    return render_template('index.html')

@app.route('/result')
def result():
    spotify_url = request.args.get('spotify_url', '')
    return render_template('result.html', spotify_url=spotify_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
