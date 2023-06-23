import time
import speech_recognition as sr


def callback(recognizer, audio):
    print('called callback')


r = sr.Recognizer()
m = sr.Microphone(device_index=0)

stop_listening = r.listen_in_background(m, callback)

print('listening')
while True:
    time.sleep(0.1)
