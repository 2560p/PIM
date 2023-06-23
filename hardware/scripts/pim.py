import time
import speech_recognition as sr
import requests


def callback(recognizer, audio):
    print('called callback')
    with open('audio/audio.m4a', 'rb') as file:  # direct input from the mic does not work
        try:
            print('got the message, awaiting the response.')
            answer = requests.post('http://127.0.0.1:5000/pim/conversation',
                                   data=file.read(),
                                   headers={'Content-Type': 'audio/wav'})
            assert answer.status_code == 200
        except Exception as e:
            print('whoopsie: ' + str(e) + '. ' + answer[1])


r = sr.Recognizer()
m = sr.Microphone()

stop_listening = r.listen_in_background(m, callback)

print('listening')
while True:
    time.sleep(0.1)
