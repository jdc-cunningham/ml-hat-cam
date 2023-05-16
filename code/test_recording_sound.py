# https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone
import pyaudio
import wave

def get_device():
  p = pyaudio.PyAudio()

  for i in range(p.get_device_count()):
    # nasty terminal dump
    if ('Lavalier' in p.get_device_info_by_index(i).get('name')):
      return i

def record_audio():
  form_1 = pyaudio.paInt16 # 16-bit resolution
  chans = 1 # 1 channel
  samp_rate = 44100 # 44.1kHz sampling rate
  chunk = 4096 # 2^12 samples for buffer
  record_secs = 10 # seconds to record
  dev_index = 1 # get_device()
  wav_output_filename = 'test1.wav' # name of .wav file

  audio = pyaudio.PyAudio() # create pyaudio instantiation

  # create pyaudio stream
  stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                      input_device_index = dev_index,input = True, \
                      frames_per_buffer=chunk)
  print("recording")
  frames = []

  # loop through stream and append audio chunks to frame array
  for ii in range(0,int((samp_rate/chunk)*record_secs)):
      data = stream.read(chunk)
      frames.append(data)

  print("finished recording")

  # stop the stream, close it, and terminate the pyaudio instantiation
  stream.stop_stream()
  stream.close()
  audio.terminate()

  # save the audio frames as .wav file
  wavefile = wave.open(wav_output_filename,'wb')
  wavefile.setnchannels(chans)
  wavefile.setsampwidth(audio.get_sample_size(form_1))
  wavefile.setframerate(samp_rate)
  wavefile.writeframes(b''.join(frames))
  wavefile.close()

record_audio()
