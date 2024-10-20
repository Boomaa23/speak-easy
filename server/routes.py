import flask
import words
import io
import os
import cartesia
import feedback
import uuid
from datetime import datetime
import json
import storage 
from googletrans import Translator
from flask import make_response, send_file, request, jsonify


api_blueprint = flask.Blueprint('api', __name__)

index_w = 0
index_p = 0


@api_blueprint.route('/api/user/speakslang', methods=['GET'])
def api_user_speaks_lang():
    user_id = request.args.get('user_id')
    language = request.args.get('language')
    user = storage.get_user_by_id(user_id=user_id)
    speaks_lang = user.speaks_lang(language)
    return speaks_lang


# Both modes: trains the voice model
@api_blueprint.route('/api/train', methods=['POST'])
def api_train():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio = request.files['audio']
    embedding_resp = cartesia.clone_voice(audio.read())
    embedding = embedding_resp.json().get("embedding")
    user_id = uuid.uuid4().hex
    #print(user_id)
    response = cartesia.create_voice(user_id, "en", embedding)
    #print(json.loads(response.content))
    voice_id = json.loads(response.content).get("id")
    is_public = json.loads(response.content).get("is_public")
    curr_time = datetime.now()
    create_user_input = {
        "user_id": user_id,
        "created_at": curr_time
    }
    voice_user_input = {
        "voice_id": voice_id,
        "user_id": user_id,
        "language": "en",
        "is_public": is_public,
        "description": f"{user_id} (en)",
        "created_at": curr_time 
    }
    if 200 <= response.status_code < 300:
        storage.create_user(create_user_input)
        storage.create_voice(voice_user_input)
        return {"user_id": response.json().get("user_id")}
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
    audio.save('last_try.mp3')
    user_transcription = feedback.transcribe_audio('last_try.mp3')

    # Retrieve and transcribe the example audio file
    correct_audio_path = "last_example.mp3"
    correct_transcription = feedback.transcribe_audio(correct_audio_path)

    # Compare transcriptions and make suggestions
    diff = feedback.compare_transcriptions(correct_transcription, user_transcription)
    suggestions = feedback.generate_suggestions(diff)
    return jsonify(suggestions)


# Communication mode: retrieves the audio clip from the user and translates into the desired language
@api_blueprint.route('/api/upload_get_translate', methods=['POST'])
def api_upload_audio_comm():
    # Retrieve the user's audio file and desired language
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio = request.files['audio']
    language = request.form.get('language', 'en')

    # Save and transcribe the audio file
    user_audio_path = os.path.join(os.path.expanduser('~'), 'last_try.mp3')
    audio.save(user_audio_path)
    user_transcription = feedback.transcribe_audio(user_audio_path)
    
    # Translate the audio file
    translator = Translator()
    translation = translator.translate(user_transcription, dest=language)

    # Retrieve the voice id of the user for the desired language
    user_id = request.form["user_id"]
    user = storage.get_user_by_id(user_id=user_id)
    if (user.speaks_lang(language)):
        voice_id = user.get_voiceid_from_lang(language)
    else:
        # FUTURE TODO: When we support training on languages other than 
        # English, change this logic to support taking base 
        # voiceids from other languages as well
        base_voice_id = user.get_voiceid_from_lang("en")
        response = cartesia.localize_voice(base_voice_id, language)
        
        # Construct input for saving this in voice db
        voice_id = json.loads(response.content).get("id")
        is_public = json.loads(response.content).get("is_public")
        curr_time = datetime.now()
        voice_user_input = {
            "voice_id": voice_id,
            "user_id": user_id,
            "language": "en",
            "is_public": is_public,
            "description": f"{user_id} (en)",
            "created_at": curr_time 
        }
        storage.create_voice(voice_user_input)

    # Create the translated version of the audio file in your voice
    tts_response = cartesia.text_to_speech(translation, voice_id, language)
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
@api_blueprint.route('/api/speak', methods=['POST'])
def api_speak():
    language = request.form.get('language', 'en')
    words = request.form.get('words', 'Hello World')
    user_id = request.form.get("user_id")
    user = storage.get_user_by_id(user_id=user_id)
    voice_id = user.get_voiceid_from_lang(language) 
    response = cartesia.text_to_speech(words, voice_id, language)

    if response.status_code == 200:
        # Save the audio clip to the root directory
        with open('last_example.mp3', 'wb') as audio_file:
            audio_file.write(response.content)

        # Send the file back in the response
        mp3_buffer = io.BytesIO(response.content)
        response = make_response(send_file(
            mp3_buffer,
            as_attachment=True,
            download_name="output.mp3",
            mimetype="audio/mpeg"
        ))
        return response
    else:
        return jsonify({"error": "Failed to generate audio",
                        "status": response.status_code, "message": response.text}), response.status_code

