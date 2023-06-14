from flask import Blueprint, request
import os
import openai
from responses import ok, err, server_err
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
conversation_page = Blueprint('conversation_page', __name__)
SPECIAL_PHRASES = {
    "how's your day": "Good, yours?"
}


@conversation_page.route('', methods=['POST'])
def post():
    prompt = request.form.get('text')

    if not prompt:
        return err("Text cannot be empty.")

    if prompt.lower() in SPECIAL_PHRASES:
        return ok(SPECIAL_PHRASES[prompt.lower()])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception:
        return server_err("An error occurred during API request")

    return ok(response.choices[0].message["content"])