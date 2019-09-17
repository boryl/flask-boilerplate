from flask import jsonify, make_response, request, abort
from flask.views import MethodView
from .models import db, Book, BookSchema, BookPostSchema, Author
from .decorators import require_token

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
            return make_response(jsonify(books_schema.dump(books).data), 200)

    @require_token
    def post(self):
        # Add new book
        payload = request.json
        new_book, errors = book_post_schema.load(payload)
        print(new_book)
        if(errors):
            abort(400, 'Can´t parse payload')

        book_author = Author.query.get(new_book.author_id)

        if book_author is None:
            abort(
                404, 'Author not found for id: {author_id}'.
                format(author_id=new_book.author_id)
                )

        db.session.add(new_book)
        db.session.commit()

        return make_response(jsonify(book_schema.dump(new_book).data), 201)


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
            return make_response(jsonify(book_schema.dump(book).data), 200)

    @require_token
    def put(self, book_id):
        # Update book
        payload = request.json

        update, errors = book_post_schema.load(payload)

        if(errors):
            abort(400, 'Can´t parse payload')

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

        return make_response(jsonify(book_schema.dump(update_book).data), 200)

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
