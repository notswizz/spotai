from generate_playlist import generate_playlist
from save_to_spotify import save_playlist_to_spotify

# Request user input for the prompt and playlist title
input_prompt = input("Enter a prompt to generate a playlist: ")
playlist_name = input("Enter a title for the playlist: ")

playlist = generate_playlist(input_prompt)
print("Generated Playlist:")
for i, song in enumerate(playlist, start=1):
    print(f"{i}. {song}")

spotify_url = save_playlist_to_spotify(playlist_name, playlist)
print(f"Playlist saved to Spotify: {spotify_url}")
