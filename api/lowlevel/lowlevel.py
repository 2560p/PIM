from flask import Blueprint, request
from responses import ok, err, server_err

from lowlevel.functions import translate

ll_endpoint = Blueprint('ll_endpoint', __name__)


@ll_endpoint.route('translate', methods=['POST'])
def respond():
    prompt = request.form.get('text')

    if not prompt:
        return err("Please input text to be translated")

    translation = translate(prompt)

    if translation[0] == 500:
        return server_err(translation[1])

    return ok(translation[1])
