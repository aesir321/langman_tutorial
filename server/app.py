from flask import Flask
from flask_restx import Resource, Api, Namespace
from flask_cors import CORS
from .util import get_config

games_api = Namespace("games", description="Creating and playing games")


@games_api.route("")
class Games(Resource):
    pass


class OneGame(Resource):
    pass


# Create the app and configure it
app = Flask(__name__)
print(list(app.config))
# TODO: This Fails because ENV is no-longer a configuration used internally by FLASK.  Check to see the docs for the
# corresponding FLASK version used in the tutorial. https://flask.palletsprojects.com/en/3.0.x/config/#builtin-configuration-values
tmp = app.config["ENV"]
app.config.update(get_config(app.config["ENV"], app.open_resource("config.yaml")))
CORS(app)
api = Api(app)
api.add_namespace(games_api, path="/api/games")
