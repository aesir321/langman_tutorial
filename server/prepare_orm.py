import csv
from sqlalchemy import create_engine
import sqlalchemy.orm
from .langman_orm import base_games, Usage, base_usage
from flask import Flask

app = Flask(__name__)
app.config.from_object("config")
app.config.from_envvar("SETTINGS_FILE")


@app.cli.command("init-db")
def init_db():
    db_usage = create_engine(app.config["DB_USAGE"])
    base_usage.metadata.create_all(db_usage)
    db_games = create_engine(app.config["DB_GAMES"])
    base_games.metadata.create_all(db_games)

    Session = sqlalchemy.orm.sessionmaker(db_usage)
    session = Session()
    if session.query(Usage).count() == 0:
        data = []
        rows = csv.reader(open("data/usages.csv", encoding="utf8"))
        for row in rows:
            if len(row[4]) <= 500:
                data.append(
                    Usage(
                        usage_id=int(row[0]),
                        language=row[1],
                        secret_word=row[3],
                        usage=row[4],
                        source=row[5],
                    )
                )
        print("Adding", len(data), "rows to Usage table")
        session.add_all(data)
        session.commit()
