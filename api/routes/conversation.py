from flask import Blueprint

import os
import openai
# from responses import ok, err, server_err

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

conversation = Blueprint('conversation', __name__)

prompt = "hello"

completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "user", "content": prompt}
  ]
)

print(completion.choices[0].message["content"])