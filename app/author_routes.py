from app import db
from app.models.author import Author
from .book_routes import validate_model
from flask import Blueprint, jsonify, request, make_response, abort


authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


@authors_bp.route("", methods=["GET"])
def get_all_authors():
    authors = Author.query.all()
    authors_response = []
    for author in authors:
        authors_response.append({
            "id": author.id,
            "name": author.name
        })
    return jsonify(authors_response)


@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)


@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):
    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=author
    )

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"New book {new_book.title} by {new_book.author.name} successfully created"), 201)


@authors_bp.route("/<author_id>/books", methods=["GET"])
def get_all_books_by_author(author_id):
    
    author = validate_model(Author, author_id)

    book_response = []
    for book in author.books:
        book_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })

    return jsonify(book_response)
