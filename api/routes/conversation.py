from flask import Blueprint, request
import os
import openai
from responses import ok, err, server_err
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
conversation_page = Blueprint('conversation_page', __name__)


@conversation_page.route('', methods=['POST'])
def post():
    prompt = request.form.get('text')

    if prompt == "":
        return err("Text cannot be empty.")
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

    if response:
        return ok(response.choices[0].message["content"])
    else:
        return err("Error occurred during API response.")
