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
                 'content': 'You are an assistant with translation to Dutch. Your name is Pim. You should always respond with "Alsjeblieft!" when someone thanks you. Otherwise, respond with a Dutch translation of the sentence. Make sure that the level of Dutch is basic, so that even a beginner can understand. You are allowed to translate to a different language besides Dutch and English ONLY if specifically asked to do so'},
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
        result = openai.Audio.transcribe(
            'whisper-1', file, prompt='disregard the coughing. focus on the actual words.').text
    except Exception:
        return (False, 'A problem has occurred')

    return (True, result)


def tts(text):
    file = io.BytesIO()
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system',
                 'content': 'Give me the internationally recognized two letter code of the language of the text that I put in and ONLY the two letter code. Make it lowercase. If you doubt - put "en".'},
                {'role': 'system', 'content': text},
            ]
        )
    except Exception:
        return (False, 'Error occurred during API response')
    lang = response.choices[0].message.content

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
    dutch = ''

    if level == "beginner":
        dutch = "A1"

    if level == "intermediate":
        dutch = "A2"

    if level == "advanced":
        dutch = "B1"

    prompt = f"Generate 10 question (one word without article - its English translation being the answer) of {dutch} level of Dutch."

    if level == "initial":
        prompt = ("Generate 10 question (one Dutch word without article - "
                  "its English translation being the answer)."
                  "Make the test volatile, starting with A1, "
                  "and finishing with B1. It should resemble the initial test "
                  "so that the user can see their progress. ")

    schema = {
        'type': 'object',
        'properties': {
            'questions': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'question': {'type': 'string'},
                        'answer': {'type': 'string'},
                    }
                },
            }
        }
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": prompt}
            ],
            functions=[
                {
                    'name': 'get_questions',
                    'parameters': schema,
                }
            ],
            function_call={'name': 'get_questions'},
        )
    except Exception:
        return (False, "Something went wrong on the server side.")

    return (True, json_loads(response.choices[0].message.function_call.arguments))


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


def mode_switcher(message):
    schema = {
        'type': 'object',
        'properties': {
            'action': {'type': 'string',
                       'description': 'Might be either "mode_switch" or "pass". Mode switch is triggered when the user is asking to change the mode to "translation" or "conversation". Pass is used in any other case.'},
            'mode': {'type': 'string',
                     'description': 'Might be either "translation" or "conversation". Only used when action is "mode_switch".'},
        },
        'required': ['action'],
    }

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-0613',
            messages=[
                {'role': 'system',
                 'content': 'Determine whether the user wants to switch the mode based on the message.'},
                {'role': 'user', 'content': message},
            ],
            functions=[{'name': 'mode_switcher', 'parameters': schema}],
            function_call={'name': 'mode_switcher'}
        )
    except Exception:
        return (False, 'An error occurred during API request')

    return (True, response.choices[0].message.function_call.arguments)
