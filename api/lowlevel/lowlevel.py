from flask import Blueprint, request
from responses import ok, err, server_err

from lowlevel.functions import translate, transcribe

ll_endpoint = Blueprint('ll_endpoint', __name__)


@ll_endpoint.route('translate', methods=['POST'])
def respond_translation():
    prompt = request.form.get('text')

    if not prompt:
        return err("Please input text to be translated")

    translation = translate(prompt)

    if translation[0] == 500:
        return server_err(translation[1])

    return ok(translation[1])


@ll_endpoint.route('transcribe', methods=['POST'])
def respond_transcription():
    if request.data == b"":
        return err("No file has been detected")

    if request.mimetype.split("/")[0] != "audio":
        return err("Invalid file format. File is not supported.")

    transcription = transcribe(request.data)

    if transcription[0] == 500:
        return server_err(transcription[1])

    return ok(transcription[1])
