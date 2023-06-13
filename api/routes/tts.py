from flask import Blueprint, request, send_file
from responses import ok, err, server_err
import requests
import io
from dotenv import load_dotenv
import os

load_dotenv()

tts_page = Blueprint('tts_page', __name__)

@tts_page.route('', methods=["POST"])
def tts(): 
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

  try:
    if lang == "en" and text != "":
      resp = requests.post(url, json=payload, headers=headers)
      file = io.BytesIO(resp.content)
      return send_file(file, mimetype="audio/mpeg", download_name='file.mp3')
    
    else:
      if lang == "" and text == "":
        raise Exception("No language specified and no text has been provided to turn into speech")
      elif lang != "en" and text == "":
        raise Exception("Language not supported yet and no text has been provivided to turn into speech")
      elif lang == "":
        raise Exception("No lnaguage specified")
      elif lang != "en":
        raise Exception("Language not supported")
      if text == "":
        raise Exception("No text has been filled in to be turned into speech")
    
  except Exception as de:
    error_message = "ERROR: " + str(de)
    print(error_message)
    return error_message
