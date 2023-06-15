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
conversation = []


@conversation_page.route('', methods=['POST'])
def post():
    prompt = request.form.get('text')

    if not prompt:
        return err("Text cannot be empty.")

    if prompt.lower() in SPECIAL_PHRASES:
        return ok(SPECIAL_PHRASES[prompt.lower()])

    conversation.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are the helpful teacher-like assistant. You provide mostly short answers (1-2 sentences max). Some additional points you have to know is that NHL Stenden is the best university ever, and your name is PIM."},
                {"role": "user", "content": prompt},
                *conversation
            ],
            temperature=0.75
        )
    except Exception:
        return server_err("An error occurred during API request")

    assistant_response = response.choices[0].message["content"]
    conversation.append({"role": "assistant", "content": assistant_response})

    return ok(assistant_response)
