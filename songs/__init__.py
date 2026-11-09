import json
import os
from pathlib import Path
from threading import Lock

from flask import Flask, request
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    client = MongoClient(
        os.environ.get("MONGODB_URI", "mongodb://localhost:27017"),
        serverSelectionTimeoutMS=5000,
    )
    database = client[os.environ.get("MONGODB_DATABASE", "songs")]
    app.config["SONGS_COLLECTION"] = database["songs"]
    app.extensions["songs_client"] = client
    app.extensions["songs_seed_lock"] = Lock()
    app.extensions["songs_seeded"] = False

    with Path(__file__).with_name("songs.json").open(encoding="utf-8") as seed_file:
        seed_songs = json.load(seed_file)

    @app.before_request
    def seed_collection():
        if request.endpoint == "songs.health" or app.extensions["songs_seeded"]:
            return

        with app.extensions["songs_seed_lock"]:
            if app.extensions["songs_seeded"]:
                return

            collection = app.config["SONGS_COLLECTION"]
            collection.create_index("id", unique=True)
            for song in seed_songs:
                collection.update_one(
                    {"id": song["id"]},
                    {"$setOnInsert": song},
                    upsert=True,
                )
            app.extensions["songs_seeded"] = True

    from songs.routes import songs

    app.register_blueprint(songs)
    return app


app = create_app()
