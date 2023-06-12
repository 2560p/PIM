from flask import Blueprint, request, send_file
from responses import ok, err, server_err
import requests
import io

tts_page = Blueprint('tts_page', __name__)

@tts_page.route('', methods=["POST"])
def tts(): 
  lang = request.form.get("lang")
  text = request.form.get("text")

  if lang == "en":
   # This is normal Marijn
    url = "https://api.elevenlabs.io/v1/text-to-speech/xEucmSu4xLB83D3WYWPa"
   
   # This is Angry/screaming Marijn
   # url = "https://api.elevenlabs.io/v1/text-to-speech/5fXNDVjFv4jo0c9LTZrT"
    
    headers = {
      'xi-api-key': '',
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

    file = io.BytesIO(resp.content)
    # file.name = "test.mp3"
    return send_file(file, mimetype="audio/mpeg", download_name='file.mp3')
  else:
    return err("lang not supported (yet)")

  