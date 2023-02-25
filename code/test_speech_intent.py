from speech_to_intent.speech_to_intent import SpeechIntent

def zoom_in():
  print("zoom in")

def zoom_out():
  print("zoom out")

speech = SpeechIntent(zoom_in, zoom_out)
speech.start_listening()
