import time
import speech_recognition as sr
import requests
import io

from pydub import AudioSegment
from pydub.playback import play


def callback(recognizer, audio):
    print('got the message, awaiting the response.')
    try:
        answer = requests.post('http://127.0.0.1:5000/pim/conversation',
                               data=audio.get_wav_data(),
                               headers={'Content-Type': 'audio/wav'})
        assert (answer.status_code == 200)
    except Exception as e:
        print('whoopsie: ' + str(e) + '. ' + answer[1])

    play(AudioSegment.from_file(io.BytesIO(answer.content), format='mp3'))


r = sr.Recognizer()
m = sr.Microphone(device_index=0)

r.energy_threshold = 1400
r.dynamic_energy_threshold = False

stop_listening = r.listen_in_background(m, callback)

print('listening')
while True:
    time.sleep(0.1)
