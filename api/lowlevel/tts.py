from flask import Blueprint, request, send_file
from responses import ok, err, server_err
import requests
import io
from dotenv import load_dotenv
import os
from gtts import gTTS

load_dotenv()

tts_page = Blueprint('tts_page', __name__)

@tts_page.route('', methods=["POST"])
def tts():
  if "lang" not in request.form and "text" not in request.form:
    return err("The language and text have not been provided")
  elif "lang" not in request.form:
    return err("The language has not been provided")
  elif "text" not in request.form:
    return err("The text has not been provided")

  lang = request.form.get("lang")
  text = request.form.get("text")

# This is normal Marijn
  url = "https://api.elevenlabs.io/v1/text-to-speech/xEucmSu4xLB83D3WYWPa"

  headers = {
    'xi-api-key': os.environ.get("ELEVENLABS_API_KEY"),
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

  if lang == "" and text == "":
    return err("No language specified and no text has been provided to turn into speech")
  elif lang != "en" and lang != "nl"and text == "":
    return err("Language not supported yet and no text has been provivided to turn into speech")
  elif lang == "":
    return err("No lnaguage specified")
  elif lang != "en" and lang != "nl":
    return err("Language not supported")
  elif text == "":
    return err("No text has been filled in to be turned into speech")

  file = io.BytesIO()

  if lang == "en":
    try:
      resp = requests.post(url, json=payload, headers=headers)
    except:
      return server_err("An error has occurred within the server")

    file.write(resp.content)
  else:
    try:
      resp = gTTS(text, lang='nl')
    except:
      return server_err("An error has occurred within the server")

    resp.write_to_fp(file)

  file.seek(0)
  return send_file(file, mimetype="audio/mpeg", download_name='file.mp3')
