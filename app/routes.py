from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, request, make_response, abort


books_bp = Blueprint("books", __name__, url_prefix="/books")


# helper function
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"Book {book_id} invalid"}, 400))
    
    book = Book.query.get(book_id)
    if not book:
        abort(make_response({"message": f"Book {book_id} not found"}, 404))
    return book

# def validate_error(request_body):
#     if not request_body["title"] or not request_body["description"]:
#         abort(make_response(({"message": "Missing title or description to update."}, 400)))
    

@books_bp.route("", methods=["POST"])
def create_books():

    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@books_bp.route("", methods=["GET"])
def get_all_books():
    title_query = request.args.get("title")

    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
        # Book.query.limit(100).all() -- limits query to 100

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)

    
@books_bp.route("/<book_id>", methods=["GET"])
def get_one_book(book_id):
    book = validate_book(book_id)
    return book.to_dict()

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()
    # validate_error(request_body)

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"message": f"Book {book_id} successfully updated."}), 200)


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book {book_id} successfully deleted."))

    








# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Title A", "Description A"),
#     Book(2, "Title B", "Description B"),
#     Book(3, "Title C", "Description C")
# ]


# @books_bp.route("", methods=["GET"])
# def get_book(book_id):
#     try:
#         book_id = int(book_id)
#         for book in books:
#             if book.id == book_id:
#                 return {
#                     "id": book.id,
#                     "title": book.title,
#                     "description": book.description
#                 }
#     except ValueError:
#         return {"message": f"Book {book_id} is invalid"}, 400
    # return {"message": f"Book {book_id} does not exist"}, 404