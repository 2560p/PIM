from flask import Blueprint, request
import openai

from responses import ok

translate_page = Blueprint('translate_page', __name__)

api_key = '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'
openai.api_key = api_key


@translate_page.route('', methods=['POST'])
def post():
    text = request.form.get('text')

    translation = translate_text(text)
    # return "Translation: " + str(dict(request.values)) + "\n"
    return ok(translation)



