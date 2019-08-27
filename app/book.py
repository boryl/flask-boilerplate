from flask import jsonify, make_response, request,  Blueprint, abort
from flask.views import MethodView
from flask import current_app as app
from .models import db, Book, BookSchema, BookPostSchema
from sqlalchemy.exc import IntegrityError

#book_bp = Blueprint('book_bp', __name__)
#book_bp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

book_post_schema = BookPostSchema()
book_schema = BookSchema()
books_schema = BookSchema(many=True)

class Books(MethodView):
	
	def get(self):
		"""
		file: static/yml/books-get.yml
		"""
		return "return all books"
	
	def post(self):
		""" Responds to POST requests """
		return "Responding to a POST request"


class Book(MethodView):
	def get(self, entity):
		""" Responds to GET requests """
		payload = request.json
		return jsonify(payload)

	

	def put(self, entity):
		""" Responds to PUT requests """
		return "Responding to a PUT request"

	def patch(self, entity):
		""" Responds to PATCH requests """
		return "Responding to a PATCH request"

	def delete(self, entity):
		""" Responds to DELETE requests """
		return "Responding to a DELETE request"



"""
##CREATE
@book_bp.route('/', methods=['POST'])
def new_book():
	payload = request.json
	
	new_book, errors = book_post_schema.load(payload)
	
	# Validate payload
	if(errors):
		abort(make_response(jsonify(error='Can´t parse payload'), 400))
	
	book_author = Author.query.get(payload['author_id'])
	
	if book_author is None:
		abort(make_response(jsonify(error='Author not found for id: {author_id}'.format(author_id=payload['author_id'])), 404))
	
	
	db.session.add(new_book)
	db.session.commit()
	
	return jsonify(book_schema.dump(new_book).data), 201



# READ
@book_bp.route('/<int:book_id>', methods=['GET'])
def list_book(book_id):
	book = Book.query.get(book_id)
	
	if book is None:
		abort(make_response(jsonify(error='Book not found for id: book_id'.format(book_id=book_id)), 404))
		
	else:
		return jsonify(book_schema.dump(book).data), 200


@book_bp.route('/', methods=['GET'])	
def list_books():
	books = Book.query.order_by(Book.title).all()
	if books is None:
		abort(make_response(jsonify(error='Books not found'), 404))
		
	else:
		return jsonify(books_schema.dump(books).data), 200
	
"""
"""
# UPDATE
@book_bp.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
	
	payload = request.json
	
	update, errors = author_schema.load(payload)
	
	if(errors):
		abort(make_response(jsonify(error='Can´t parse payload'), 400))
	
	update_author = Author.query.get(author_id)
	
	if update_author is None:
		abort(make_response(jsonify(error='Author not found for id: {author_id}'.format(author_id=author_id)), 404))
	
	else:
		update.id = update_author.id
		try:
			db.session.merge(update)
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			abort(make_response(jsonify(error='Author {name} exists already'.format(name=payload['name'])), 409))

		return jsonify(author_schema.dump(update).data), 200
		
		

# DELETE
@book_bp.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
	
	# Get the person requested
	author = Author.query.get(author_id)

	# Did we find a person?
	if author is None:
		abort(make_response(jsonify(error='Author not found for id: {author_id}'.format(author_id=author_id)), 404))
	else:
		db.session.delete(author)
		db.session.commit()
		return make_response(jsonify(message='Author {id} deleted'.format(id=author_id)), 200)
"""