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
    #print(embedding_resp.content)
    embedding = json.loads(embedding_resp.content).get("embedding")
    #embedding = embedding_resp.json().get("embedding")
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
        return {"user_id": user_id}
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
    correct_audio_path = "audio_phrase_learn.mp3"
    correct_transcription = feedback.transcribe_audio(correct_audio_path)

    # Compare transcriptions and make suggestions
    diff = feedback.compare_transcriptions(correct_transcription, user_transcription)
    suggestions = feedback.generate_suggestions(diff)
    return suggestions


# Communication mode: retrieves the audio clip from the user and translates into the desired language
@api_blueprint.route('/api/upload_get_translate', methods=['POST'])
def api_upload_audio_comm():
    # Retrieve the user's audio file and desired language
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio = request.files['audio']
    language = request.form.get('language', 'en').lower()

    # Save and transcribe the audio file
    user_audio_path = os.path.join(os.path.expanduser('~'), 'last_try.mp3')
    audio.save(user_audio_path)
    user_transcription = feedback.transcribe_audio(user_audio_path)
    
    # Translate the audio file
    translator = Translator()
    translation_raw = translator.translate(user_transcription, dest=language)
    translation = translation_raw.text
    print(user_transcription)
    print(translation)
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
        print(f"language: {language}, base voice id: {base_voice_id}")
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
    print(f"translation: {translation}\n voice_id: {voice_id}\n language: {language}")
    tts_response = cartesia.text_to_speech(translation, voice_id, language)
    #print(tts_response.content)
    with open ('audio_result.mp3', 'wb') as f:
        f.write(tts_response.content)
    return send_file('audio_result.mp3',  mimetype='audio/mpeg')


# Learning Mode: retrieves the next word to practice
@api_blueprint.route('/api/nextword', methods=['POST'])
def api_get_next_word():
    global index_w
    i = index_w % 10
    language = request.form.get('language', 'en')
    index_w += 1
    result_word = words.practice_word(i, language)
    result_word_en = words.practice_word(i, 'en')
    return {"phrase": result_word, "phrase_en": result_word_en}


# Learning Mode: retrieves the next phrase to practice
@api_blueprint.route('/api/nextphrase', methods=['POST'])
def api_get_next_phrase():
    global index_p
    i = index_p % 10
    language = request.form.get('language', 'en')
    print(f'language: {language}')
    index_p += 1
    result_phrase = words.practice_phrase(i, language)
    result_phrase_en = words.practice_phrase(i, 'en')
    return {"phrase": result_phrase, "phrase_en": result_phrase_en}


# Learning Mode: Stores and returns a given phrase in a given language
# must supply the following inputs:
# words = the phrase to be spoken
# user_id = the unique id of the consumer
# language = the language of words (the language the result will be spoken in)
@api_blueprint.route('/api/speak', methods=['POST'])
def api_speak():
    language = request.form.get('language', 'en')
    words = request.form.get('words', 'Hello World')
    user_id = request.form.get("user_id")
    user = storage.get_user_by_id(user_id=user_id)
    voice_id = user.get_voiceid_from_lang(language) 
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
    print(f"words: {words}\n voice_id: {voice_id}\n language: {language}")
    tts_response = cartesia.text_to_speech(words, voice_id, language)
    with open ('audio_phrase_learn.mp3', 'wb') as f:
        f.write(tts_response.content)
    return send_file('audio_phrase_learn.mp3',  mimetype='audio/mpeg')
