from flask import Blueprint, request, send_file
from responses import ok, err, server_err

from lowlevel.functions import translate, transcribe, tts, quiz, conversation

ll_endpoint = Blueprint('ll_endpoint', __name__)


@ll_endpoint.route('translate', methods=['POST'])
def respond_translation():
    prompt = request.form.get('text')

    if not prompt:
        return err('Please input text to be translated')

    translation = translate(prompt)

    if not translation[0]:
        return server_err(translation[1])

    return ok(translation[1])


@ll_endpoint.route('transcribe', methods=['POST'])
def respond_transcription():
    if request.data == b'':
        return err('No file has been detected')

    if request.mimetype.split('/')[0] != 'audio':
        return err('Invalid file format. File is not supported.')

    transcription = transcribe(request.data)

    if not transcription[0]:
        return server_err(transcription[1])

    return ok(transcription[1])


@ll_endpoint.route('tts', methods=['POST'])
def respond_tts():
    lang = request.form.get('lang')
    text = request.form.get('text')

    if not lang and not text:
        return err('The language and text have not been provided')
    elif not lang:
        return err('The language has not been provided')
    elif not text:
        return err('The text has not been provided')

    if lang not in ['en', 'nl']:
        return err('The language is not supported')

    answer = tts(lang, text)

    if not answer[0]:
        return server_err(answer[1])

    return send_file(answer[1], mimetype='audio/mpeg', download_name='file.mp3')


@ll_endpoint.route('quiz', methods=['POST'])
def respond_quiz():
    level = request.form.get('level')

    if not level:
        return err('No level has been provided')

    if level not in ['initial', 'beginner', 'intermediate', 'advanced']:
        return err('Invalid level has been provided')

    answer = quiz(level)

    if not answer[0]:
        return server_err(answer[1])

    return ok(answer[1])


@ll_endpoint.route('conversation', methods=['POST'])
def respond_conversation():
    message = request.form.get('message')

    if not message:
        return err("Text cannot be empty.")

    answer = conversation(message)

    if not answer[0]:
        return server_err(answer[1])

    return ok(answer[1])
