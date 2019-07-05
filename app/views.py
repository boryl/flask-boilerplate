from flask import Blueprint
from .models import Author
from app import db


author_bp = Blueprint('author', __name__)

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
	authors_dict = {}
	try:
		authors = Author.query.all()
		for author in authors:
			authors_dict.update( {'name' : author.name} )
	except Exception as e:
		print("Failed to query DB")
		print(e)
		
	return authors_dict