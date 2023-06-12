from flask import Blueprint, request

import os
import openai
# from responses import ok, err, server_err

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

conversation_page = Blueprint('conversation', __name__)


@conversation_page.route('', methods=['POST'])
def post():
    prompt = request.form.get('text')

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # print(completion.choices[0].message["content"])

    return completion.choices[0].message["content"]
