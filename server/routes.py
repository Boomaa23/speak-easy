import flask

api_blueprint = flask.Blueprint('api', __name__)


@api_blueprint.route('/api/eggs', methods=['GET'])
def api_get_eggs():
    return "eggs"
