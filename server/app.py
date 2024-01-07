from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restx import Resource, Api, Namespace
from flask_cors import CORS
from .langman_orm import Usage

games_api = Namespace("games", description="Creating and playing games")


@games_api.route("")
class Games(Resource):
    def post(self):
        """
        Create a new game and return the game id
        """
        num_games = g.usage_db.query(Usage).count()
        return {"message": f"Games POST under construction - {num_games} games"}


@games_api.route("/<game_id>")
class OneGame(Resource):
    def get(self, game_id):
        """
        Get the state of the game
        """
        return {"message": "Game GET under construction"}

    def put(self, game_id):
        """
        Guess a letter and update the game state accordingly.
        """
        return {"message": "Game PUT under construction"}

    def delete(self, game_id):
        """
        End the game, delete the record
        """
        return {"message": "Game delete under construction"}


# Create the app and configure it
app = Flask(__name__)
app.config.from_object("default_config")
app.config.from_envvar("SETTINGS_FILE")
CORS(app)
api = Api(app)
api.add_namespace(games_api, path="/api/games")


@app.before_request
def init_db():
    """
    Initialise the database by creating the global db_session

    This gets decorated with @app.before_request to run on each request
    """
    if not hasattr(g, "usage_db"):
        db_usage = create_engine(app.config["DB_USAGE"])
        g.usage_db = sessionmaker(db_usage)()

    if not hasattr(g, "games_db"):
        db_games = create_engine(app.config["DB_GAMES"])
        g.games_db = sessionmaker(db_games)()


@app.teardown_request
def close_db(exception):
    """
    Close down the db connection, same on cannot be used b/w threads

    This gets decorated with @app.teardown_request to close the connection to the db after each request.
    """
    if hasattr(g, "usage_db"):
        g.usage_db.close()
        _ = g.pop("usage_db")

    if hasattr(g, "games_db"):
        g.games_db.close()
        _ = g.pop("games_db")
