from flask import Blueprint

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Title A", "Description A"),
    Book(2, "Title B", "Description B"),
    Book(3, "Title C", "Description C")
]

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/<book_id>")
def get_book(book_id):
    try:
        book_id = int(book_id)
        for book in books:
            if book.id == book_id:
                return {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                }
    except ValueError:
        return {"message": f"Book {book_id} is invalid"}, 400
    return {"message": f"Book {book_id} does not exist"}, 404