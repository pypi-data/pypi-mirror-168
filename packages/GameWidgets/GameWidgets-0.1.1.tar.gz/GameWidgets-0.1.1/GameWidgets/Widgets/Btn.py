import pygame
pygame.init()
class Normal_Btn:
    def __init__(self,screen,fgcolor=(255,255,255),xy=(0,0),font='freesansbold.ttf',size=20,text='Custom Button',Outline=(255,255,255),Thickness=5):
        self.screen=screen
        self.BG=(0,255,0)
        self.FG=fgcolor
        self.xy=xy
        self.size=size
        self.font=font
        self.text=text
        self.TH=Thickness
        TextFont=pygame.font.SysFont(self.font,self.size)
        self.text=TextFont.render(self.text,self.BG,self.FG)
        self.ROutline=self.text.get_rect(topleft=self.xy)
        self.COutline=Outline
        
    def Draw(self):
        self.screen.blit(self.text,self.xy)
        pygame.draw.rect(self.screen,self.COutline,self.ROutline,self.TH)
    def Detect(self,mousexy,event):
        x=mousexy[0]
        y=mousexy[1]
        if ((x>=self.ROutline.topleft[0]) and (x<=self.ROutline.bottomright[0])) and ((y>=self.ROutline.topleft[1]) and (y<=self.ROutline.bottomright[1])):
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                return True
            else:
                return False
        else:
            return False
class Active_Btn:
    def __init__(self,screen,Colors=(),text='Active Button',**kwarg):
        self.Startup=False
        self.Width=0
        self.Height=0
        self.Colors=Colors
        self.text=text
        self.font='freesansbold.ttf'
        self.size=50
        self.x=0
        self.y=0
        for key,val in kwarg.items():
            if key=='Width':
                self.Startup=True
                self.Width=val
            elif key=='Height':
                self.Startup=True
                self.Height=val
            elif key=='Font':
                self.font=val
            elif key=='Size':
                self.size=val
            elif key=='X':
                self.x=val
            elif key=='Y':
                self.y=val
            else:
                print('Btn.py')
                print(f'Value Error! No Attribute to {key}')
        self.font=pygame.font.SysFont(self.font,self.size)
        self.label=self.font.render(self.text,self.Colors[3],self.Colors[4])
        self.rect=self.label.get_rect(topleft=(self.x,self.y))
        self.surf=pygame.Surface((self.rect.width,self.rect.height))
        self.state=0
        self.screen=screen
    def Detect(self,mousexy,event):
        x=mousexy[0]
        y=mousexy[1]
        if ((x>=self.rect.topleft[0]) and (x<=self.rect.bottomright[0])) and ((y>=self.rect.topleft[1]) and (y<=self.rect.bottomright[1])):
            if event.type==pygame.MOUSEBUTTONDOWN:
                self.state=2
                return True
            else:
                self.state=1
                return False
        else:
            self.state=0
            return False
    def Draw(self):
        self.surf.fill(self.Colors[self.state])
        self.screen.blit(self.surf,self.rect.topleft)
        self.screen.blit(self.label,self.rect.topleft)
        
