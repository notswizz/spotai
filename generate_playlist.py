import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_playlist(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"generate 13 songs that follow the prompt: {prompt}",
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].text.strip().split("\n")
