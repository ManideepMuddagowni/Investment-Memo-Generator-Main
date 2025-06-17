import os
import requests
from dotenv import load_dotenv

load_dotenv()
EURI_API_KEY = os.getenv("EURI_API_KEY")

def call_ai_agent(prompt, model="gpt-4.1-nano", max_tokens=700, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {EURI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    response = requests.post(
        "https://api.euron.one/api/v1/euri/alpha/chat/completions",
        json=payload,
        headers=headers
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']
