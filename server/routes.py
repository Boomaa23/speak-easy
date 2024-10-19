import flask
import request
import jsonify
import words
import os

UPLOAD_FOLDER = 'test'
api_blueprint = flask.Blueprint('api', __name__)

index_w = 0
index_p = 0


@api_blueprint.route('/api/eggs', methods=['GET'])
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

@api_blueprint.route('/api/say', methods=['GET'])
def api_say():
    