from flask import Blueprint, request
from responses import ok, err, server_err

import openai
from dotenv import load_dotenv
import os
import io

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

stt_page = Blueprint('stt_page', __name__)
# stt_page.config = {}
# stt_page.config['UPLOAD_EXTENSIONS'] = ['.m4a']

@stt_page.route('', methods=["POST"])
def transcribe():    
  try:
    # file = request.files['file']
    file = io.BytesIO(request.data)
    file.name = "something.mp3"

    result = openai.Audio.transcribe("whisper-1", file).text
    return ok(result)
  except Exception as err:
    return err(err)
