# https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()

with sr.Microphone(device_index=1) as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    print("Vosk thinks you said " + r.recognize_vosk(audio))
except sr.UnknownValueError:
    print("Vosk could not understand audio")
except sr.RequestError as e:
    print("Vosk error; {0}".format(e))
