from flask import Blueprint, request

post_page = Blueprint('post_page', __name__)

@post_page.route('', methods=['POST'])
def post():
    return "post data: " + str(dict(request.values)) + "\n"
