from flask import Blueprint, jsonify, abort, make_response, request
from flask import current_app as app
from .models import db, Author, AuthorSchema
from sqlalchemy.exc import IntegrityError

author_bp = Blueprint('author_bp', __name__)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)



##CREATE
@author_bp.route('/', methods=['POST'])
def new_author():
	payload = request.json
	
	new_author, errors = author_schema.load(payload)
	
	# Validate payload
	if(errors):
		abort(make_response(jsonify(error='Can´t parse payload'), 400))
	
	try:
		db.session.add(new_author)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		abort(make_response(jsonify(error='Author {name} exists already'.format(name=payload['name'])), 409))
	
	return jsonify(author_schema.dump(new_author).data), 201



# READ
@author_bp.route('/<int:author_id>', methods=['GET'])
def list_author(author_id):
	author = Author.query.get(author_id)
	
	if author is None:
		abort(make_response(jsonify(error='Author not found for id: {author_id}'.format(author_id=author_id)), 404))
		
	else:
		return jsonify(author_schema.dump(author).data), 200


@author_bp.route('/', methods=['GET'])	
def list_authors():
	authors = Author.query.order_by(Author.name).all()
	if authors is None:
		abort(make_response(jsonify(error='Authors not found'), 404))
		
	else:
		return jsonify(authors_schema.dump(authors).data), 200
	


# UPDATE
@author_bp.route('/<int:author_id>', methods=['PUT'])
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
@author_bp.route('/<int:author_id>', methods=['DELETE'])
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
		
		
