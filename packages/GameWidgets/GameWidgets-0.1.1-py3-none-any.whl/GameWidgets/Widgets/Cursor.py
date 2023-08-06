import pygame
pygame.init()
class Rect_Cursor:
    def __init__(self,screen,Color=(255,0,0),**kwarg):
        self.Color=Color
        self.screen=screen
        self.Outline=0
        self.Width=20
        self.Height=20
        self.screen=screen
        for key,value in kwarg.items():
            if key=='Outline':
                self.Outline=value
                #print(self.Outline)
            elif key=='Width':
                self.Width=value
            elif key=='Height':
                self.Height=value
            else:
                print('Cursor.py')
                print(f'Value Error! No Attribute to {key}')
                quit()
        
        mouse=pygame.mouse.get_pos()
        self.x=mouse[0]
        self.y=mouse[1]
        self.rect=pygame.Rect(self.x,self.y,self.Width,self.Height)
    def Draw(self):
        mouse=pygame.mouse.get_pos()
        self.x=mouse[0]
        self.y=mouse[1]
        self.rect.center=(self.x,self.y)
        pygame.draw.rect(self.screen,self.Color,self.rect,self.Outline)
