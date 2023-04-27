import os
import requests

DALLE_API_KEY = os.environ["OPENAI_API_KEY"]
DALLE_API_URL = "https://api.openai.com/v1/images/generations"

def generate_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DALLE_API_KEY}",
    }

    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "256x256",
    }

    response = requests.post(DALLE_API_URL, json=data, headers=headers)
    response.raise_for_status()

    image_url = response.json()["data"][0]["url"]
    return image_url
