from flask import current_app as app
from flask import Blueprint, make_response, jsonify

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
	return 'Homepage'

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
		
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)