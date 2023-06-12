from flask import Blueprint, request
from responses import ok, err, server_err

tts_page = Blueprint('tts_page', __name__)


@tts_page.route('', methods=["POST"])
def tts(text):
  #text is the text thats gonna be turned into speech using 11labs.
  #return ok("yey")
  #PostForm needs to be changed to the variable which holds either nl or en, since we ened to know whether the text is in Dutch or English
if PostForm == 'en':
  api_key = 'MY KEY'

  api_url = "https://api.elevenlabs.ai/speech"

  headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
  }

  payload = {
    "text" = text,
    "voice_id": "xEucmSu4xLB83D3WYWPa",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
      "stability": 75,
      "similarity_boost": 75
    }
  }
  
  response = requests.post(api_url, json=payload, headers=headers)




  
 
  if PostForm == 'nl':
    response = requests.post(api_url, json=payload)
    
    