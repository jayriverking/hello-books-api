from app import db
from app.models.genre import Genre
from app.models.book import BookGenre
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

@genre_bp.route("", methods=["POST"])
def make_a_genre():
    response_body = request.get_json()
    new_genre = Genre(name=response_body["name"])
    db.session.add(new_genre)
    db.session.commit()
    return make_response(jsonify(f"Genre {new_genre.name} successfully created"), 201)

@genre_bp.route("/<genre_id>/books", methods=["POST"])
def create_book(genre_id):
    genre = validate_model(Genre, genre_id)
    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author_id=request_body["author_id"],
        genres=[genre]
    )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)


# @genre_bp.route("/<genre_id>/books", methods=["GET"])
# def get_all_books(genre_id):
#     genre = validate_model(Genre, genre_id)
#     genre_response = []
#     for book in genre:
#         genre_response.append({
#             book.to_dict()
#         })

#     return jsonify(genre_response)

@genres_bp.route("/<genre_id>/books", methods=["GET"])
def read_all_books(genre_id):
    
    genre = validate_model(Genre, genre_id)

    books_response = []
    for book in genre.books:
        books_response.append(
            book.to_dict()
        )
    return jsonify(books_response)