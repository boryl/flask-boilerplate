from flask import Blueprint
from .models import Author

author_bp = Blueprint('author', __name__)

@author_bp.route('/author/new')
def new_author():
  """Creates a new author by a giving name (via GET parameter)
  e.g.: GET /author/new?name=Francisco creates a author named Francisco
  """
  #author = Author(name=request.args.get('name', ''))
  #author.save()
  return 'Saved :)'

@author_bp.route('/authors/')
def list_authors():
  """List all authors.     
  e.g.: GET /authors"""
  #authors = Author.query.all()
  content = '<p>Authors:</p>'
  #for author in authors:
  #   content += '<p>%s</p>' % author.name
  return content
