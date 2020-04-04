import http
import json

from flask import Blueprint, current_app, request

from model import Book
from serializer import BookSchema

bp_books = Blueprint("books", __name__)


@bp_books.route("/", methods=["GET", "POST"])
@bp_books.route("/<int:book_id>", methods=["PUT", "DELETE"])
def books(book_id=None):
    if request.method == "GET":
        bs = BookSchema(many=True)
        result = Book.query.all()
        return bs.jsonify(result), http.HTTPStatus.OK
    elif request.method == "POST":
        bs = BookSchema()
        book = bs.load(request.json)
        current_app.db.session.add(book)
        current_app.db.session.commit()
        return bs.jsonify(book), http.HTTPStatus.CREATED
    elif request.method == "DELETE":
        if book_id:
            book = Book.query.filter(Book.id == book_id)
            book.delete()
            current_app.db.session.commit()
            return "", http.HTTPStatus.NO_CONTENT
    elif request.method == "PUT":
        if book_id:
            bs = BookSchema()
            book = Book.query.filter(Book.id == book_id)
            book.update(request.json)
            current_app.db.session.commit()
            return bs.jsonify(book.first()), http.HTTPStatus.OK
