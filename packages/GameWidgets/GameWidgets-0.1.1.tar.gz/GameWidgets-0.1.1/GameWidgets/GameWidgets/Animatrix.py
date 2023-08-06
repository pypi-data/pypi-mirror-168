import pygame
import time
class Animation:
    def __init__(self,screen,Location=(0,0),Pictures=(),S_Per_Frame=0.1,FSize=()):
        self.S=screen
        #self.loc=Location
        self.rects=[]
        self.images=[]
        iteration=0
        for path in Pictures:
            image=pygame.image.load(path)
            tuple=FSize[iteration]
            image=pygame.transform.scale(image,tuple)
            image=pygame.Surface.convert_alpha(image)
            rect=image.get_rect(center=Location)
            self.rects.append(rect)
            self.images.append(image)
            iteration+=1
        self.playing=False
        self.FPS=S_Per_Frame
        self.nImages=len(self.images)
        self.index=0
    def Start(self):
        if self.playing:
            return
        self.playing=True
        self.imageStartTime=time.time()
        self.index=0
    def Update(self):
        if not self.playing:
            return
        self.elapsed=time.time()-self.imageStartTime
        if self.elapsed<self.imageStartTime:
            if self.index!=0:
                pygame.time.delay(self.FPS)
            self.index+=1
            if self.index<self.nImages:
                self.imageStartTime=time.time()
            else:
                self.playing=False
                self.index=0
    def draw(self):
        theimage=self.images[self.index]
        self.S.blit(theimage,self.rects[self.index])