import openai

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def translate(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an assistant with translation to Dutch. Your name is Pim. You should always respond with \"Alsjeblieft!\" when someone thanks you. Otherwise, respond with a Dutch translation of the sentence. Make sure that the level of Dutch is basic, so that even a beginner can understand."},
                {"role": "system", "content": prompt},
            ]
        )
    except Exception:
        return (500, "Error occurred during API response")

    return (200, response.choices[0].message.content)
