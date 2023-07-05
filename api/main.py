from flask import Blueprint, request, send_file
from lowlevel.functions import conversation, translate, transcribe, tts, mode_switcher

from responses import ok, err, server_err

from base64 import b64encode, b64decode
from json import loads as json_loads

main_endpoint = Blueprint('main_endpoint', __name__)


@main_endpoint.route('', methods=['POST'])
def pim_sequence():
    if not request.form.get('audio'):
        return err('No audio was provided')

    transcription = transcribe(b64decode(request.form.get('audio')))

    if not transcription[0]:
        return server_err(transcription[1])

    mode = request.form.get('mode')

    message = transcription[1]

    if not mode:
        switch = mode_switcher(message)

        if not switch[0]:
            return server_err(switch[1])

        switch = json_loads(switch[1])

        if switch['action'] == 'mode_switch':
            return ok({'mode_switch': {'mode': switch['mode']}})
        else:
            return err('No mode selected')

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
        answer = tts(data[1])
    else:
        answer = tts(data[1])

    if not answer[0]:
        return server_err(answer[1])

    audio = b64encode(answer[1].getvalue())
    return ok({'data': data[1], 'audio': audio.decode('ascii')})
