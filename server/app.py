import datetime
import uuid
from flask import Flask, g
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from flask_restx import Resource, Api, Namespace
from flask_cors import CORS
from .langman_orm import Game, Usage, User

games_api = Namespace("games", description="Creating and playing games")


@games_api.route("")
class Games(Resource):
    valid_langs = ("en", "es", "fr")

    def post(self):
        """
        Create a new game and return the game id

        :route: ``/`` GET

        :payload:
            * ``username`` A string containing the player's name
            * ``language`` Language to play in (e.g., "en")

        :returns:
            A success message:
                * ``message`` Literal "success"
                * ``game_id`` The new game's UUID
        """
        # check input is valid
        if not (
            games_api.payload
            and "username" in games_api.payload
            and "language" in games_api.payload
        ):
            games_api.abort(400, "New game POST requires username and language")
        lang = games_api.payload["language"]
        name = games_api.payload["username"]
        user_id = str(uuid.uuid3(uuid.NAMESPACE_URL, name))
        if lang not in self.valid_langs:
            return {
                "message": f"New game POST language must be from {Games.valid_langs}"
            }, 400

        # if user does not exist, create user; get user id
        user = g.games_db.query(User).filter(User.user_id == user_id).one_or_none()
        if user is None:
            user = User(
                user_id=user_id,
                user_name=name,
                first_time=datetime.datetime.now(),
            )
            g.games_db.add(user)
            g.games_db.commit()
            user = g.games_db.query(User).filter(User.user_name == name).one()
        user._game_started(lang)

        # select a usage example
        usage = (
            g.usage_db.query(Usage)
            .filter(Usage.language == lang)
            .order_by(func.random())
            .first()
        )

        # create the new game
        new_game_id = str(uuid.uuid4())
        new_game = Game(
            game_id=new_game_id,
            player=user.user_id,
            usage_id=usage.usage_id,
            bad_guesses=0,
            reveal_word="_" * len(usage.secret_word),
            start_time=datetime.datetime.now(),
        )
        g.games_db.add(new_game)
        g.games_db.commit()

        return {"message": "success", "game_id": new_game_id}

    def delete(self, game_id):
        """Delete record for game ``game_id``

        Args:
            game_id (str): DELETE

        Returns:
            str: An acknowledgement object:
                * ```message`` Either "One" or "Zero" records deleted.

        This method removed the game from its table
        """
        game = g.games_db.query(Game).filter(Game.game_id == game_id).one_or_none()
        if game is not None:
            g.games_db.delete(game)
            g.games_db.commit()
            message = "One record deleted"
        else:
            message = "Zero records deleted"
        return {"message": message}


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
