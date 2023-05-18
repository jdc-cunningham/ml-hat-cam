import pygame

class Sound:
  def __init__(self):
    pygame.mixer.init()

    self.playing_sound = False

  def play_sound_file(self, sound_file):
    self.playing_soudn = True
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy() == True:
      continue

    self.playing_sound = False
