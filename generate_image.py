import os
import requests
import json

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def generate_image_url(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        "model": "image-alpha-001",
        "prompt": f"{prompt}",
        "num_images":1,
        "size":"256x256",
        "response_format":"url"
    }

    response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
    response_data = json.loads(response.text)

    if response.status_code == 200 and response_data['data']:
        return response_data['data'][0]['url']
    else:
        print("Error generating image:", response.text)
        return None
