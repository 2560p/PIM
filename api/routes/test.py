from flask import Blueprint
from responses import ok, err, server_err

test_page = Blueprint('test_page', __name__)

@test_page.route('/success')
def success():
    return ok({'message': 'success'})

@test_page.route('/error')
def error():
    return err({'message': 'error'})

@test_page.route('/server_error')
def server_error():
    return server_err({'message': 'server_error'})
