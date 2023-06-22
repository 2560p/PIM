import openai
import io
import requests

from gtts import gTTS

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


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
        return (500, 'Error occurred during API response')

    return (200, response.choices[0].message.content)


def transcribe(data):
    file = io.BytesIO(data)
    file.name = 'something.mp3'

    try:
        result = openai.Audio.transcribe('whisper-1', file).text
    except Exception:
        return (500, 'A problem has occurred')

    return (200, result)


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
            return (500, 'An error has occurred within the server')
    else:
        try:
            resp = gTTS(text, lang=lang)
        except Exception:
            return (500, 'An error has occurred within the server')

        resp.write_to_fp(file)

    file.seek(0)
    return (200, file)
