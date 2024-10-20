import dotenv
import flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from routes import api_blueprint


dotenv.load_dotenv()
app = flask.Flask(__name__)
CORS(app)

app.register_blueprint(api_blueprint)


@app.teardown_appcontext
def close_connection(exception):
    # TODO documentation
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # Start with the correct headers and status code from the error
    response = e.get_response()
    # Replace the body with JSON
    response.data = flask.json.dumps(
        flask.jsonify(
            e.code,
            {
                'name': e.name,
                'description': e.description,
            },
        ),
        indent=4,
    )
    response.content_type = 'application/json'
    return response
