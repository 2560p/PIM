from flask import Blueprint, request
from lowlevel.functions import conversation, translate, transcribe, tts

from responses import err, server_err

main_endpoint = Blueprint('main_endpoint', __name__)


@main_endpoint.route('<mode>', methods=['POST'])
def pim_sequence(mode):
    if request.data == b'':
        return err('No file has been detected')

    if request.mimetype.split('/')[0] != 'audio':
        return err('Invalid file format. File is not supported.')

    transcription = transcribe(request.data)

    if not transcription[0]:
        return server_err(transcription[1])

    message = transcription[1]

    match mode:
        case 'conversation':
            data = conversation(message)
        case 'translation':
            data = translate(message)
        case _:
            return err('Invalid mode')

    if not data[0]:
        return err(data[1])

    if mode == 'conversation':
        answer = tts('en', data[1])
    else:
        answer = tts('nl', data[1])

    if not answer[0]:
        return err(answer[1])

    return answer[1]
