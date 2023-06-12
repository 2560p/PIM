from flask import Blueprint

import os
import openai
# from responses import ok, err, server_err

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

conversation = Blueprint('conversation', __name__)

prompt = "hello"

# Generate a completion
response = openai.Completion.create(
    engine='davinci-codex',
    prompt=prompt,
    max_tokens=100
)

# Extract the generated text from the response
generated_text = response.choices[0].text.strip()

# Print the generated completion
print(generated_text)