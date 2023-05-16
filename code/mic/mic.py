# https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone
import pyaudio
import wave

class Mic:
  def __init__(self,  usb_path):
    self.recordpath = usb_path
    self.recording = False
    self.stop_recording = False
    self.stream = None
    self.audio = None
    self.form_1 = pyaudio.paInt16 # 16-bit resolution
    self.chans = 1 # 1 channel
    self.samp_rate = 44100 # 44.1kHz sampling rate
    self.chunk = 4096 # 2^12 samples for buffer
    self.record_secs = 21600 # seconds to record, insane here 6 hours
    self.dev_index = 1 # get_device()

  def scan_devices(self):
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
      # nasty terminal dump
      if ('Lavalier' in p.get_device_info_by_index(i).get('name')):
        return i

  def start_recording(self, file_name):
    self.filename = file_name
    self.audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    self.stream = self.audio.open(format = self.form_1, rate = self.samp_rate, channels = self.chans, \
                        input_device_index = self.dev_index, input = True, \
                        frames_per_buffer = self.chunk)
    
    self.recording = True

    self.frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((self.samp_rate/self.chunk)*self.record_secs)):
      if (self.stop_recording):
        self.recording = False
        self.stop_recording()
        return

      data = self.stream.read(self.chunk)
      self.frames.append(data)

  def stop_recording(self):
    # stop the stream, close it, and terminate the pyaudio instantiation
    self.stream.stop_stream()
    self.stream.close()
    self.audio.terminate()

    wav_output_filename = self.recordpath + self.filename + '.wav'

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(self.chans)
    wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
    wavefile.setframerate(self.samp_rate)
    wavefile.writeframes(b''.join(self.frames))
    wavefile.close()
