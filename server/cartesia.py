import os
import json
import dotenv
import requests

dotenv.load_dotenv()
_REQUEST_HEADERS = {
    'Cartesia-Version': '2024-10-19',
    'X-API-Key': os.getenv('CARTESIA_API_KEY'),
}


def text_to_speech(text, voice_id, language):
    return _cartesia_request(
        '/tts/bytes',
        data=json.dumps({
            'model_id': ('sonic-english' if language == 'en' else 'sonic-multilingual'),
            'transcript': text,
            'voice': {
                'mode': 'id',
                'id': voice_id,
            },
            'output_format': {
                'container': 'mp3',
                'bit_rate': 128000,
                'sample_rate': 44100,
                'encoding': 'pcm_f32le'
            },
            'language': language
        }),
        method='POST',
        headers = {
            'Cartesia-Version': '2024-10-19',
            'X-API-Key': os.getenv('CARTESIA_API_KEY'),
            "Content-Type": "application/json"
        }
    )


def clone_voice(audio_bytes):
    return _cartesia_request(
        '/voices/clone/clip',
        files={'clip': audio_bytes},
        data={'enhance': "true"},
        method='POST',
        headers = _REQUEST_HEADERS
    )


def localize_voice(voice_id, target_language):
    original_voice = _cartesia_request(
        f'/voices/{voice_id}',
        method='GET',
        headers = _REQUEST_HEADERS
    )
    og_voice = json.loads(original_voice.content)
    localized_embedding = _cartesia_request(
        '/voices/localize',
        data=json.dumps({
            'embedding': og_voice.get('embedding'),
            'language': target_language,
            'original_speaker_gender': 'male',  # TODO auto-select for female speakers
            #'dialect': 'us'
        }),
        method='POST',
        headers = {
            'Cartesia-Version': '2024-10-19',
            'X-API-Key': os.getenv('CARTESIA_API_KEY'),
            "Content-Type": "application/json"
        }
    ).json()

    localized_voice = create_voice(og_voice.get('name'), target_language, localized_embedding['embedding'])

    return localized_voice


def create_voice(name, language, embedding):
    return _cartesia_request(
        '/voices',
        data= json.dumps({
            'name': name,
            'description': f'{name} ({language})',
            'embedding': embedding,
            'language': language,
        }),
        method='POST',
        headers = {
            'Cartesia-Version': '2024-10-19',
            'X-API-Key': os.getenv('CARTESIA_API_KEY'),
            "Content-Type": "application/json"
        }
    )


def _cartesia_request(endpoint, method='GET', **kwargs):
    return requests.request(
        method=method,
        url=f'https://api.cartesia.ai{endpoint}',
        **kwargs
    )
