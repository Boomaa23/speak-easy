from cartesia import Cartesia
import os
import requests

CARTESIA_API_KEY = "3ed9262d-677f-4a76-920d-683b6d51ce38"

#client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

# Clone a voice using filepath
url = "https://api.cartesia.ai/voices/clone/clip"
files = { "clip": "open('<clone_voice.mp3>', 'rb')" }
payload = { "enhance": "true" }
headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": "3ed9262d-677f-4a76-920d-683b6d51ce38"
}
response = requests.post(url, data=payload, files=files, headers=headers)
print(response.json())
