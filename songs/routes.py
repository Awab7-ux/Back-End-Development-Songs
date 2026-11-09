from flask import Blueprint, Response, current_app, jsonify, request
from pymongo.errors import DuplicateKeyError
from bson import json_util


songs = Blueprint("songs", __name__)


def _collection():
    return current_app.config["SONGS_COLLECTION"]


def _json_response(data, status=200):
    return Response(
        json_util.dumps(data),
        status=status,
        mimetype="application/json",
    )


def _song_payload():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None
    if not isinstance(payload.get("id"), int) or isinstance(payload.get("id"), bool):
        return None
    if not isinstance(payload.get("title"), str) or not isinstance(
        payload.get("lyrics"), str
    ):
        return None
    return payload


@songs.get("/health")
def health():
    return jsonify({"status": "OK"}), 200


@songs.get("/count")
def count_songs():
    return _json_response({"count": _collection().count_documents({})})


@songs.get("/song")
def get_songs():
    documents = list(_collection().find().sort("id", 1))
    return _json_response({"songs": documents})


@songs.get("/song/<int:song_id>")
def get_song(song_id):
    document = _collection().find_one({"id": song_id})
    if document is None:
        return _json_response({"message": "song with id not found"}, 404)
    return _json_response(document)


@songs.post("/song")
def create_song():
    payload = _song_payload()
    if payload is None:
        return jsonify({"message": "invalid song"}), 400

    collection = _collection()
    if collection.find_one({"id": payload["id"]}, {"_id": 1}) is not None:
        return jsonify(
            {"Message": f"song with id {payload['id']} already present"}
        ), 302

    try:
        result = collection.insert_one(payload)
    except DuplicateKeyError:
        return jsonify(
            {"Message": f"song with id {payload['id']} already present"}
        ), 302
    return _json_response({"inserted id": result.inserted_id}, 201)


@songs.put("/song/<int:song_id>")
def update_song(song_id):
    payload = _song_payload()
    if payload is None:
        return jsonify({"message": "invalid song"}), 400

    collection = _collection()
    update_fields = {key: value for key, value in payload.items() if key != "id"}
    result = collection.update_one({"id": song_id}, {"$set": update_fields})
    if result.matched_count == 0:
        return _json_response({"message": "song not found"}, 404)

    return _json_response(collection.find_one({"id": song_id}))


@songs.delete("/song/<int:song_id>")
def delete_song(song_id):
    result = _collection().delete_one({"id": song_id})
    if result.deleted_count == 0:
        return _json_response({"message": "song not found"}, 404)
    return "", 204
