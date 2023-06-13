from flask import Blueprint, request
from responses import ok, err, server_err
from dotenv import load_dotenv

import openai
import os
import io

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


transcribe_page = Blueprint('transcribe_page', __name__)


@transcribe_page.route('', methods=["POST"])
def transcribe():
    if request.data == b"":
        return err("No file has been detected")
    
    file = io.BytesIO(request.data)
    file.name = "something.mp3"

    try:
        result = openai.Audio.transcribe("whisper-1", file).text
    except:
        return server_err("A problem has occurred")

    return ok(result)
