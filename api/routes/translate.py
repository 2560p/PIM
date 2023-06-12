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


def translate_text(text, target_language):
    prompt = f"Translate the following English text to {target_language}: '{text}'"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    translated_text = response.choices[0].text.strip()
    return translated_text