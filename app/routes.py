from flask import Blueprint, request


main_bp = Blueprint('main_bp', __name__)


def num_to_excel_col(n):
    if n < 1:
        raise ValueError("Number must be positive")
    result = ""
    while True:
        if n > 26:
            n, r = divmod(n - 1, 26)
            result = chr(r + ord('A')) + result
        else:
            return chr(n + ord('A') - 1) + result


@main_bp.route('/')
def home():
    data = request.get_json()
    return num_to_excel_col(data['to_excel'])
