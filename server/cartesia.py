import os
import requests

_REQUEST_HEADERS = {
    'Cartesia-Version': '2024-10-19',
    'X-API-Key': os.getenv('CARTESIA_API_KEY'),
}

def text_to_speech(text, voice_id, language):
    return _cartesia_request(
        '/tts/bytes',
        payload={
            'model_id': ('sonic-english' if language == 'en' else 'sonic-multilingual'),
            'transcript': text,
            'voice': {
                'mode': 'id',
                'id': voice_id,
            },
            'output_format': {
                'container': 'mp3',
                'bit_rate': 320000,
                'sample_rate': 44100
            },
            'language': language
        },
        method='POST'
    )

def clone_voice(audio_pcm):
    return _cartesia_request(
        '/voices/clone/clip',
        files=audio_pcm,
        payload={'enhance': True},
        method='GET'
    )

def localize_voice(voice_id, target_language):
    original_voice = _cartesia_request(
        f'/voices/get/{voice_id}',
        method='GET'
    ).json()

    localized_embedding = _cartesia_request(
        '/voices/localize',
        payload={
            'embedding': original_voice['embedding'],
            'language': target_language,
            'original_speaker_gender': 'male',  # TODO auto-select for female speakers
            'dialect': 'us'
        },
        method='POST'
    ).json()

    localized_voice = _cartesia_request(
        '/voices/create',
        payload={
            'name': original_voice['name'],
            'description': f'{original_voice["name"]} (localized to {target_language})',
            'embedding': localized_embedding['embedding'],
            'language': target_language,
        },
        method='POST'
    )

    return localized_voice


def _cartesia_request(endpoint, files=None, payload=None, method='GET'):
    return requests.request(
        method=method,
        url=f'https://api.cartesia.ai{endpoint}',
        headers=_REQUEST_HEADERS,
        files=files,
        data=payload,
    )
