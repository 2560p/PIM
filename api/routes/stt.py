from flask import Blueprint, request
from responses import ok, err, server_err
from dotenv import load_dotenv

import openai
import os
import io

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

stt_page = Blueprint('stt_page', __name__)

@stt_page.route('', methods=["POST"])
def transcribe():    
  try:
    file = io.BytesIO(request.data)
    file.name = "something.mp3"

    result = openai.Audio.transcribe("whisper-1", file).text
    return ok(result)
  except Exception as err:
    return err(err)
