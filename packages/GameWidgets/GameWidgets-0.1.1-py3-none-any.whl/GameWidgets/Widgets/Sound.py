from pygame import mixer
mixer.init()
class Sound:
    def __init__(self,Sound_File=''):
        self.sound=mixer.music.load(Sound_File)
    def Play(self,Times=0,Volume=0.7):
        mixer.music.set_volume(Volume)
        mixer.music.play(Times)