import time
import speech_recognition as sr
import requests
import io
from base64 import b64decode, b64encode

from pydub import AudioSegment
from pydub.playback import play

MODE = ''


def callback(recognizer, audio):
    print('Recognizing...')
    global MODE

    data = {
        'audio': b64encode(audio.get_wav_data()).decode('ascii'),
        'mode': MODE,
    }

    try:
        resp = requests.post(
            'http://127.0.0.1:5000/pim',
            data=data,
        )
    except Exception:
        print('Failed to get the response from the server')
        return

    if resp.status_code != 200:
        print(resp.json()['errors'])
        return

    if resp.json()['data'].get('mode_switch'):
        MODE = resp.json()['data']['mode_switch']['mode']
        print(f'{MODE.capitalize()} mode activated.')
        return

    print('Got audio response. Playing...')
    play(AudioSegment.from_file(io.BytesIO(
        b64decode(resp.json()['data']['audio'])), format='mp3'))
    print('Done.\n\n')

    print('Listening...')


r = sr.Recognizer()
m = sr.Microphone(device_index=0)

r.energy_threshold = 1400
r.dynamic_energy_threshold = False

stop_listening = r.listen_in_background(m, callback)

print('This is PIM.')
print('There are two modes PIM can work in:')
print('1. Conversation mode')
print('2. Translation mode\n')

time.sleep(2)

print('Change the mode by saying the word "conversation" or "translation".')

time.sleep(2)

print('Listening...')
while True:
    time.sleep(0.1)
