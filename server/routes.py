import flask
import request
import jsonify
import words
import io
import os
from storage import create_user, create_voice
from googletrans import Translator
from flask import make_response, send_file
from cartesia import text_to_speech, clone_voice, localize_voice
from feedback import transcribe_audio, compare_transcriptions, generate_suggestions

UPLOAD_FOLDER = 'test'
api_blueprint = flask.Blueprint('api', __name__)

index_w = 0
index_p = 0

@api_blueprint.route('/api/', methods=['GET'])
def api_get_eggs():
    return "eggs"

# Both modes: trains the voice model
@api_blueprint.route('/api/train', methods=['POST'])
def api_train():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    audio_pcm = None #TODO convert audio to PCM
    response = clone_voice(audio_pcm)
    if response.status_code == 200:
        create_user(response.json())
        create_voice(response.json())
    else:
        return jsonify({"error": "Failed to clone voice", "status": response.status_code, "message": response.text}), response.status_code
    

# Learning mode: retrieves the audio clip from the user and creates feedback for them
@api_blueprint.route('/api/upload_get_feedback', methods=['POST'])
def api_upload_audio_learn():
    # Retrieve the user's audio file
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio = request.files['audio']

    # Save and transcribe the audio file
    user_audio_path = os.path.join(os.path.expanduser('~'), 'last_try.mp3')
    audio.save(user_audio_path)
    user_transcription = transcribe_audio(user_audio_path)

    # Retrieve and transcribe the example audio file
    correct_audio_path = "last_example.mp3"
    correct_transcription = transcribe_audio(correct_audio_path)

    # Compare transcriptions and make suggestions
    diff = compare_transcriptions(correct_transcription, user_transcription)
    suggestions = generate_suggestions(diff)
    return jsonify(suggestions)

# Communication mode: retrieves the audio clip from the user and translates into the desired language
@api_blueprint.route('/api/upload_get_translate', methods=['POST'])
def api_upload_audio_comm():
    # Retrieve the user's audio file and desired language
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio = request.files['audio']
    language = request.args.get('language', 'en')

    # Save and transcribe the audio file
    user_audio_path = os.path.join(os.path.expanduser('~'), 'last_try.mp3')
    audio.save(user_audio_path)
    user_transcription = transcribe_audio(user_audio_path)
    
    # Translate the audio file
    translator = Translator()
    translation = translator.translate(user_transcription, dest=language)

    # Retrieve the voice id of the user for the desired language
    # TODO get user id from frontend to get voiceid from storage
    user_id = None
    voice_id = None

    # Create the translated version of the audio file in your voice
    tts_response = text_to_speech(translation, voice_id, language)
    return tts_response

# Learning Mode: retrieves the next word to practice
@api_blueprint.route('/api/nextword', methods=['GET'])
def api_get_next_word():
    global index_w
    i = index_w % 10
    language = request.args.get('language', 'en')
    index_w += 1
    return jsonify(words.practice_word(i, language))

# Learning Mode: retrieves the next phrase to practice
@api_blueprint.route('/api/nextphrase', methods=['GET'])
def api_get_next_phrase():
    global index_p
    i = index_p % 10
    language = request.args.get('language', 'en')
    index_p += 1
    return jsonify(words.practice_phrase(i, language))

# Learning Mode: Stores and returns a given phrase in a given language
@api_blueprint.route('/api/speak', methods=['GET'])
def api_speak():
    language = request.args.get('language', 'en')
    words = request.args.get('words', 'Hello World')
    # TODO get user ID from frontend to get voice id from storage
    voice_id = None  
    response = text_to_speech(words, voice_id, language)

    if response.status_code == 200:
        # Save the audio clip to the root directory
        output_file_path = os.path.join(os.path.expanduser('~'), 'last_example.mp3')  # This saves to your home directory
        with open(output_file_path, 'wb') as audio_file:
            audio_file.write(response.content)

        # Send the file back in the response
        mp3_buffer = io.BytesIO(response.content)
        response = make_response(send_file(mp3_buffer, as_attachment=True, download_name="output.mp3", mimetype="audio/mpeg"))
        return response
    else:
        return jsonify({"error": "Failed to generate audio", "status": response.status_code, "message": response.text}), response.status_code

