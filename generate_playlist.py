import openai
import re

def generate_playlist(prompt):
    openai.api_key = "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"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate a playlist of 13 songs based on the following theme: {prompt}",
        max_tokens=260,
        n=1,
        stop=None,
        temperature=0.7,
    )

    raw_playlist = response.choices[0].text.strip().split("\n")
    playlist = [re.sub(r'^\d+\.\s', '', song) for song in raw_playlist]
    return playlist

