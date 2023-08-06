import pygame
pygame.init()
class Clock:
    def __init__(self,FPS=60):
        self.FPS=FPS
    def Set_Up_Clock(self):
        self.clock=pygame.time.Clock()
    def Set_FPS(self):
        self.clock.tick(self.FPS)
    def Set_Delay(self,TIME=1,**kwarg):
        time=TIME
        Unit=1
        for key,val in kwarg.items():
            if key=='Milli':
                Unit=1000
            else:
                print('Clock.py')
                print(f'Value Error! No Attribute to {key}')
            if Unit==1000:
                pygame.time.delay(time)
            else:
                pygame.time.delay(time*1000)
