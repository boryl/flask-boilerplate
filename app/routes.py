from flask import current_app as app
from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
	return 'Homepage'
