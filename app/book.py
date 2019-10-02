'''
    File name: book.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: API template
'''

from flask import jsonify, make_response, abort
from flask.views import MethodView
from .models import db, Book, BookSchema, BookPostSchema, Author
from .decorators import require_token, validate

book_post_schema = BookPostSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Operations on all books
class BooksApi(MethodView):
    @require_token
    def get(self):
        """
        file: static/yml/books-get.yml
        """
        # Get all books
        books = Book.query.order_by(Book.title).all()
        if books is None:
            abort(404, 'Books not found')
        else:
            return make_response(jsonify(books_schema.dump(books)), 200)

    @require_token
    @validate(book_post_schema)
    def post(self, new_book):
        # Add new book
        book_author = Author.query.get(new_book.author_id)

        if book_author is None:
            abort(
                404, 'Author not found for id: {author_id}'.
                format(author_id=new_book.author_id)
                )

        db.session.add(new_book)
        db.session.commit()

        return make_response(jsonify(book_schema.dump(new_book)), 201)


# Operations on a single book
class BookApi(MethodView):
    @require_token
    def get(self, book_id):
        # Get one book
        book = Book.query.get(book_id)

        if book is None:
            abort(
                404, 'Book not found for id {id}'
                .format(id=book_id), 404
                )
        else:
            return make_response(jsonify(book_schema.dump(book)), 200)

    @require_token
    @validate(book_post_schema)
    def put(self, update, book_id):
        # Update book
        update_book = Book.query.get(book_id)
        book_author = Author.query.get(update.author_id)

        if update_book is None:
            abort(
                404, 'Book not found for id {id}'.
                format(id=book_id)
            )
        elif book_author is None:
            abort(
                404, 'Author not found for id: {id}'.
                format(id=update.author_id)
                )
        else:
            update.id = update_book.id
            db.session.merge(update)
            db.session.commit()

        return make_response(jsonify(book_schema.dump(update_book)), 200)

    @require_token
    def delete(self, book_id):
        # Delete book
        book = Book.query.get(book_id)
        if book is None:
            abort(
                404, 'Book not found for id: {id}'.
                format(id=book_id)
            )
        else:
            db.session.delete(book)
            db.session.commit()
            return make_response(
                jsonify(message='Book {id} deleted'
                        .format(id=book_id)), 200)
