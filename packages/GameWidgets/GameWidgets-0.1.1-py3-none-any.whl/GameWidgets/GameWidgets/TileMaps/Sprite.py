import pygame
pygame.init()
class Player:
    def __init__(self,screen):
        self.screen=screen
    def StartUp(self,img='Assets/Heart.png',xy=(100,100)):
        self.Surf=pygame.image.load(img)
        self.Rect=self.Surf.get_rect(topleft=xy)
    def Scale(self,ScaleSize=(50,50)):
        self.Surf=pygame.transform.scale(self.Surf,ScaleSize)
    def Collide(self,list=[]):
        YN=self.Rect.collidelist(list)
        if YN!=None:
            return True
        else:
            return False
    def Draw(self):
        self.screen.blit(self.Surf,self.Rect)