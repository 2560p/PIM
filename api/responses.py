from flask import jsonify

# this exists to make it easier to return JSON responses.
# it also helps with consistency.
# TODO: docs for the API (responses, where, why, how, etc.)

def ok(data):
    return jsonify({'success': True, 'data': data}), 200

def err(err):
    return jsonify({'success': False, 'errors': err}), 400

def server_err(err):
    return jsonify({'success': False, 'errors': err}), 500
