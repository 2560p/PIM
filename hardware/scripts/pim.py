import time
import speech_recognition as sr
import requests
import io
from base64 import b64decode, b64encode

from pydub import AudioSegment
from pydub.playback import play

MODE = ''
quiz = {}
quiz_position = -1


def callback(recognizer, audio):
    print('Recognizing...')
    global MODE
    global quiz
    global quiz_position

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

    if MODE == 'quiz':
        if quiz_position == -1:
            data = 'You have entered the quiz mode. You are going to be provided with 10 words in Dutch to translate to English. Please, wait for a bit while I\'m preparing the quiz for you. You can always ask to exit the quiz mode.'
            resp = requests.post(
                'http://127.0.0.1:5000/ll/tts',
                data={'text': data},
            )

            if resp.status_code != 200:
                print(resp.json()['errors'])
                return

            play(AudioSegment.from_file(io.BytesIO(
                b64decode(resp.json()['data']['audio'])), format='mp3'))

            resp = requests.get(
                'http://127.0.0.1:5000/ll/quiz',
                level='initial',
            )

            if resp.status_code != 200:
                print(resp.json()['errors'])
                return

            quiz = resp.json()['data']['questions']
            quiz_position = 0

            data = 'Respond with "start" to start the quiz.'
            resp = requests.post(
                'http://127.0.0.1:5000/ll/tts',
                data={'text': data},
            )

            if resp.status_code != 200:
                print(resp.json()['errors'])
                return

            play(AudioSegment.from_file(io.BytesIO(
                b64decode(resp.json()['data']['audio'])), format='mp3'))

            quiz_position += 1

            return

        if quiz_position != 0:
            resp = requests.post(
                'http://127.0.0.1:5000/ll/check_translation',
                data={'word': quiz[quiz_position - 1]['question'],
                      'translation': quiz[quiz_position - 1]['answer']},
            )

            if resp.status_code != 200:
                print(resp.json()['errors'])
                return

            if resp.json()['data']:
                data = 'Correct!'
                resp = requests.post(
                    'http://127.0.0.1:5000/ll/tts',
                    data={'text': data},
                )

                if resp.status_code != 200:
                    print(resp.json()['errors'])
                    return

                play(AudioSegment.from_file(io.BytesIO(
                    b64decode(resp.json()['data']['audio'])), format='mp3'))

                quiz_position += 1
            else:
                data = 'Incorrect! Try again.'
                resp = requests.post(
                    'http://127.0.0.1:5000/ll/tts',
                    data={'text': data},
                )

                if resp.status_code != 200:
                    print(resp.json()['errors'])
                    return

                play(AudioSegment.from_file(io.BytesIO(
                    b64decode(resp.json()['data']['audio'])), format='mp3'))

        data_question = "Translate the followind word into ducth"
        data_word = quiz[quiz_position]['question']

        resp_question = requests.post(
            'http://127.0.0.1:5000/ll/tts',
            data={'text': data_question},
        )

        resp_word = requests.post(
            'http://127.0.0.1:5000/ll/tts',
            data={'text': data_word},
        )

        if resp_question.status_code != 200 or resp_word.status_code != 200:
            print(resp.json()['errors'])
            return

        play(AudioSegment.from_file(io.BytesIO(
            b64decode(resp_question.json()['data']['audio'])), format='mp3'))

        play(AudioSegment.from_file(io.BytesIO(
            b64decode(resp_word.json()['data']['audio'])), format='mp3'))

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
