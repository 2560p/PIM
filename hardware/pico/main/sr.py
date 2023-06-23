import urequests
import ujson
import machine
import time
import uaudio
import ubinascii

# Configure your Flask endpoint URL
ENDPOINT_URL = "http://127.0.0.1:5000"

# Configure the catchphrase you want to use
CATCHPHRASE = "Hello pim"

# Configure the microphone
SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2
MIC_PIN = 34

# Configure the LED to indicate recording status
LED_PIN = 2
led = machine.Pin(LED_PIN, machine.Pin.OUT)


# Generate a unique file name for each recording
def generate_filename():
    timestamp = int(time.time())
    filename = "recording_{}.wav".format(timestamp)
    return filename


# Start recording audio
def start_recording():
    led.on()
    audio = uaudio.Recorder(SAMPLE_RATE, SAMPLE_WIDTH, MIC_PIN)
    filename = generate_filename()
    audio.start(filename)
    print("Recording started: {}".format(filename))
    return audio


# Stop recording audio
def stop_recording(audio):
    audio.stop()
    led.off()
    print("Recording stopped")


# Send audio file to Flask endpoint
def send_audio(filename):
    with open(filename, "rb") as f:
        audio_data = f.read()

    headers = {"Content-Type": "audio/wav"}
    response = urequests.post(ENDPOINT_URL, headers=headers, data=audio_data)

    if response.status_code == 200:
        print("Audio sent to Flask endpoint successfully")
        # Perform any further actions based on the response if needed
    else:
        print("Error occurred while sending audio to Flask endpoint")


# Main loop
def main():
    audio = None
    while True:
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            print("Woke up from deep sleep")
        print("Listening for catchphrase...")
        while True:
            audio = start_recording()
            time.sleep(0.5)  # Adjust the delay between recordings as needed
            stop_recording(audio)
            send_audio(audio.filename)
            if CATCHPHRASE in audio.filename:
                break
            time.sleep(1)  # Adjust the delay between recordings as needed


# Run the main loop
main()
