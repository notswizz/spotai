import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_playlist(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Generate a playlist of 20 songs including the song title and the artist's name, based on the following theme: {prompt}. Please format the output as 'Song Title - Artist Name'.",
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].text.strip().split("\n")
