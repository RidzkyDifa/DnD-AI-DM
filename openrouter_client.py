import requests
import os
from dotenv import load_dotenv

load_dotenv()  # baca file .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_openrouter(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-2.5-flash-image-preview:free",  # bisa diganti model lain
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"OpenRouter Error {response.status_code}: {response.text}")
    data = response.json()
    return data["choices"][0]["message"]["content"]
