from flask import Flask
from flask_restplus import Resource, Api, Namespace
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
app.config.update(get_config(app.config["ENV"], app.open_resource("config.yaml")))
CORS(app)
api = Api(app)
api.add_namespace(games_api, path="/api/games")
