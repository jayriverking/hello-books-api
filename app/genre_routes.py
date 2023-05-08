from app import db
from app.models.genre import Genre
from .book_routes import validate_model
from flask import Blueprint, abort, make_response, jsonify, request

genre_bp = Blueprint("genres", __name__, url_prefix="/genres")


@genre_bp.route("", methods=["GET"])
def get_all_genre():
    genres = Genre.query.all()
    genres_response = []
    for genre in genres:
        genres_response.append({
            "id": genre.id,
            "name": genre.name
        })
    return jsonify(genres_response)

@ genre_bp.route("", methods=["POST"])
def make_a_genre():
    response_body = request.get_json()
    new_genre = Genre(name=response_body["name"])
    db.session.add(new_genre)
    db.session.commit()
    return make_response(jsonify(f"Genre {new_genre.name} successfully created"), 201)