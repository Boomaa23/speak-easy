import sys
import os
import requests

# Get the current directory of the script (sandbox.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the server directory to sys.path
server_dir = os.path.abspath(os.path.join(current_dir, '..', 'server'))
sys.path.append(server_dir)

from feedback import transcribe_audio, compare_transcriptions, generate_suggestions

CARTESIA_API_KEY_2 = "a1b1697a-174b-4afc-8720-b48feca19d51"

#client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

def test_clone():
    # Clone a voice using filepath
    url = "https://api.cartesia.ai/voices/clone/clip"
    
    # Open the audio file in binary read mode
    with open('clone_voice.mp3', 'rb') as file:
        files = { "clip": file }
        payload = { "enhance": "true" }
        
        headers = {
            "Cartesia-Version": "2024-06-10",
            "X-API-Key": CARTESIA_API_KEY_2
        }
        response = requests.post(url, data=payload, files=files, headers=headers)
    print(response.status_code)  # To print the status code
    print(response.json()) 

def test_feedback():
    # test feedback on improving pronounciation
    audio_kentucky = r"C:\Users\mzayd\Downloads\School\CalHacks11\speak-easy\test\kentucky_testing.wav"
    audio_hindi = r"C:\Users\mzayd\Downloads\School\CalHacks11\speak-easy\test\hindi_testing.wav"
    kentucky_transcribe = transcribe_audio(audio_kentucky)
    hindi_transcribe = transcribe_audio(audio_hindi)
    diff = compare_transcriptions(kentucky_transcribe, hindi_transcribe)
    suggestions = generate_suggestions(diff)
    print(suggestions)


#test_feedback()
test_clone()