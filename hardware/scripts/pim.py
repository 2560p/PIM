import time
import speech_recognition as sr
import requests
import io

from pydub import AudioSegment
from pydub.playback import play

MODE = ''


def callback(recognizer, audio):
    print('Recognizing...')
    global MODE

    try:
        resp = requests.post(
            'http://127.0.0.1:5000/ll/transcribe',
            data=audio.get_wav_data(),
            headers={'Content-Type': 'audio/wav'})

        assert resp.status_code == 200
    except Exception:
        return

    words = resp.json()['data'].lower().replace(
        '.', '').replace(',', '').replace('?', '').split(' ')

    if 'conversation' in words:
        MODE = 'conversation'
        print('Conversation mode activated.')
        return

    if 'translation' in words:
        MODE = 'translation'
        print('Translation mode activated.')
        return

    if not MODE:
        print('No mode selected.')
        return

    endpoint = 'http://127.0.0.1:5000/pim/'
    match MODE:
        case 'conversation':
            endpoint += 'conversation'
            print('Getting the conversation response...')
        case 'translation':
            endpoint += 'translation'
            print('Getting the translation response...')

    try:
        answer = requests.post(endpoint,
                               data=audio.get_wav_data(),
                               headers={'Content-Type': 'audio/wav'})

        assert answer.status_code == 200
    except Exception:
        print('Failed to get the response from the server')

    print('Playing the sound...')
    play(AudioSegment.from_file(io.BytesIO(answer.content), format='mp3'))
    print('done.\n\n')
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
