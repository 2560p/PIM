from flask import Blueprint, request
from responses import ok, err, server_err

from dotenv import load_dotenv
from json import loads as json_loads

import openai
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

quiz_page = Blueprint('quiz_page', __name__)


@quiz_page.route('', methods=["POST"])
def get_quiz():
    level = request.form.get("level")

    if not level:
        return err("no level provided.")

    if level not in ["initial", "begginer", "intermediate", "advanced"]:
        return err("invalid level provided.")

    return ok(get_questions(level))


def get_questions(level):
    prompt = ("You generate a quiz to test user's abilities in Dutch. "
              "It is a JSON array with 10 objects of type "
              "{\"question\": \"...\", \"answer\": \"...\"}. "
              "Question is a word in Dutch, and answer"
              "is the English translation. "
              "Also skip the articles.")

    if level == "initial":
        prompt += ("Make the test volatile, starting with A1, "
                   "and finishing with B1. It should resemble the initial test"
                   "so that the user can see their progress.")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return json_loads(response.choices[0].message["content"])
