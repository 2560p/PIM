from flask import jsonify

# this exists to make it easier to return JSON responses.
# it also helps with consistency.
# TODO: docs for the API (responses, where, why, how, etc.)


def ok(data):
    response = jsonify({'success': True, 'data': data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.status_code = 200
    return response


def err(err):
    response = jsonify({'success': False, 'errors': err})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.status_code = 400
    return response


def server_err(err):
    response = jsonify({'success': False, 'errors': err})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.status_code = 500
    return response
