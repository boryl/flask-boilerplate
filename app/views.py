from flask import Blueprint, jsonify
from .models import Author, AuthorSchema
from app import db


author_bp = Blueprint('author', __name__)

author_schema = AuthorSchema()

@author_bp.route('/author/new')
def new_author():
	try:
		author = Author(name='Jane')
		db.session.add(author)
		db.session.commit()
	except Exception as e:
		print("Failed to add book")
		print(e)
		
	return 'Saved :)'

@author_bp.route('/authors/')
def list_authors():
	author = Author.query.filter_by(id=1).first()
	if author is None:
		response = {
			'message': 'author does not exist'
		}
		return jsonify(response), 404
	result = author_schema.jsonify(author)
	response= {
		'data': result,
		'status_code' : 202
	}
	return jsonify(response)