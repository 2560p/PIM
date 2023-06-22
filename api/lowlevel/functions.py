import openai
import io
import requests

from gtts import gTTS
from json import loads as json_loads

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

chat_history = []


def translate(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system',
                 'content': 'You are an assistant with translation to Dutch. Your name is Pim. You should always respond with "Alsjeblieft!" when someone thanks you. Otherwise, respond with a Dutch translation of the sentence. Make sure that the level of Dutch is basic, so that even a beginner can understand.'},
                {'role': 'system', 'content': prompt},
            ]
        )
    except Exception:
        return (False, 'Error occurred during API response')

    return (True, response.choices[0].message.content)


def transcribe(data):
    file = io.BytesIO(data)
    file.name = 'something.mp3'

    try:
        result = openai.Audio.transcribe('whisper-1', file).text
    except Exception:
        return (False, 'A problem has occurred')

    return (True, result)


def tts(lang, text):
    file = io.BytesIO()

    if lang == 'en':
        try:
            url = 'https://api.elevenlabs.io/v1/text-to-speech/xEucmSu4xLB83D3WYWPa'
            headers = {
                'xi-api-key': os.environ.get('ELEVENLABS_API_KEY'),
                'Content-Type': 'application/json'
            }

            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75
                }
            }

            resp = requests.post(url, json=payload, headers=headers)
            file.write(resp.content)
        except Exception:
            return (False, 'An error has occurred within the server')
    else:
        try:
            resp = gTTS(text, lang=lang)
        except Exception:
            return (False, 'An error has occurred within the server')

        resp.write_to_fp(file)

    file.seek(0)
    return (True, file)


def quiz(level):
    prompt = ("You generate a quiz to test user's abilities in Dutch. "
              "It is a JSON array with 10 objects of type "
              "{\"question\": \"...\", \"answer\": \"...\"}. "
              "Question is a word in Dutch, and answer"
              "is the English translation. "
              "Also skip the articles. ")

    if level == "initial":
        prompt += ("Make the test volatile, starting with A1, "
                   "and finishing with B1. It should resemble the initial test "
                   "so that the user can see their progress. ")

    if level == "beginner":
        prompt += "Aim for the A1 level."

    if level == "intermediate":
        prompt += "Aim for the A2 level."

    if level == "advanced":
        prompt += "Aim for the B1 level."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
    except Exception:
        return (False, "Something went wrong on the server side.")

    return (True, json_loads(response.choices[0].message["content"]))


def conversation(message):
    global conversation
    chat_history.append({'role': 'user', 'content': message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "You are the helpful teacher-like assistant. You provide mostly short answers (1-2 sentences max). Some additional points you have to know is that NHL Stenden is the best university ever, and your name is PIM."},
                *chat_history
            ],
            temperature=0.75
        )
    except Exception:
        return (False, "An error occurred during API request.")

    assistant_response = response.choices[0].message["content"]
    chat_history.append({'role': 'assistant', 'content': assistant_response})

    return (True, assistant_response)
