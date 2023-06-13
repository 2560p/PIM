from flask import Blueprint, request
import openai
import os
from dotenv import load_dotenv
from responses import ok, err, server_err

translate_page = Blueprint('translate_page', __name__)

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


@translate_page.route('', methods=['POST'])
def post():
    prompt = request.form.get('text')

    if not prompt:
        return err("Please input text to be translated")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an assistant with translation to Dutch. Your name is Pim. You should always respond with \"Alsjeblieft!\" when someone thanks you. Otherwise, respond with a Dutch translation of the sentence. Make sure that the level of Dutch is basic, so that even a beginner can understand."},
                {"role": "system", "content": prompt},
            ]
        )
    except:
        return server_err("Error occurred during API response")

    return ok(response.choices[0].message.content)
