from flask import Blueprint, request
import openai
import os
from dotenv import load_dotenv

from responses import ok

translate_page = Blueprint('translate_page', __name__)

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


@translate_page.route('', methods=['POST'])
def post():
    text = request.form.get('text')

    translation = translate_text(text)
    # return "Translation: " + str(dict(request.values)) + "\n"
    return ok(translation)


def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are an assistant with translation to Dutch. Your name is Pim. You should always respond with \"Alsjeblieft!\" when someone thanks you. Otherwise, respond with a Dutch translation of the sentence. Make sure that the level of Dutch is basic, so that even a beginner can understand."},
            {"role": "system", "content": text},
        ]
    )

    return response.choices[0].message.content