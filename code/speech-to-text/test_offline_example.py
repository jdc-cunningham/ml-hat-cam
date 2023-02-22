# https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__main__.py
import speech_recognition as sr

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
  # print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# device_index=1

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
