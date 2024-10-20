import os

import dotenv
import flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from routes import api_blueprint
from storage import db


dotenv.load_dotenv()
app = flask.Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/db.db'  # In-memory DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create all database tables within the app context
with app.app_context():
    db.create_all()

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

#TODO: ADD DB!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!