import flask
import request
import jsonify
import words
import cartesia
import io
import os
from flask import make_response, send_file

UPLOAD_FOLDER = 'test'
api_blueprint = flask.Blueprint('api', __name__)

index_w = 0
index_p = 0


@api_blueprint.route('/api/', methods=['GET'])
def api_get_eggs():
    return "eggs"

@api_blueprint.route('/api/uploadtraining', methods=['POST'])
def api_upload_training_data():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']

    if audio.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the audio file
    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    audio.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

@api_blueprint.route('/api/nextword', methods=['GET'])
def api_get_next_word():
    global index_w
    i = index_w % 10
    language = request.args.get('language', 'en')
    index_w += 1
    return words.practice_word(i, language)

@api_blueprint.route('/api/nextphrase', methods=['GET'])
def api_get_next_phrase():
    global index_p
    i = index_p % 10
    language = request.args.get('language', 'en')
    index_p += 1
    return words.practice_phrase(i, language)

@api_blueprint.route('/api/speak', methods=['GET'])
def api_speak():
    language = request.args.get('language', 'en')
    words = request.args.get('words', 'Hello World') 
    voice_id = None # ADD LOGIC TO RETRIEVE voice_id FROM SMIT DB
    response = cartesia.text_to_speech(words, voice_id, language)
    if response.status_code == 200:
        mp3_buffer = io.BytesIO(response.content)
        response = make_response(send_file(mp3_buffer, as_attachment=True, download_name="output.mp3", mimetype="audio/mpeg"))
        return response
    else:
        return jsonify({"error": "Failed to generate audio", "status": response.status_code, "message": response.text}), response.status_code
    