import pygame
import GameWidgets
pygame.init()
class Simple_YN:
    def __init__(self,Text='',**kwarg):
        self.text=Text
        self.BG=(0,0,0)
        self.FG=(255,255,255)
        self.size=(200,250)
        self.font='freesansbold'
        self.NO_Size=50
        self.YES_Size=50
        self.YES_POS=(100,50)
        self.NO_POS=(0,50)
        self.TextSize=50
        self.Title='Simple Dialoge Box'
        for key,item in kwarg.items():
            if key=='BG':
                self.BG=item
            elif key=='FG':
                self.FG=item
            elif key=='Size':
                self.size=item
            elif key=='Font':
                self.font=item
            elif key=='Title':
                self.Title=item
            elif key=='NO_Size':
                self.NO_Size=item
            elif key=='YES_Size':
                self.YES_Size=item
            elif key=='NO_POS':
                self.NO_POS=item
            elif key=='YES_POS':
                self.YES_POS=item
        

    def Pop_Up(self):
        screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.Title)
        font=pygame.font.SysFont(self.font,self.TextSize)
        show=font.render(self.text,self.BG,self.FG)
        NO=GameWidgets.Btn.Normal_Btn(screen,
                                           fgcolor=self.FG,
                                           xy=self.NO_POS,
                                           font=self.font,
                                           size=self.NO_Size,
                                           text=' No ')
        YES=GameWidgets.Btn.Normal_Btn(screen,
                                            fgcolor=self.FG,
                                            xy=self.YES_POS,
                                            font=self.font,
                                            size=self.YES_Size,
                                            text=' Yes ')
        run=True
        force=False
        val=None
        while run:
            screen.fill((0,0,0))
            screen.blit(show,(0,0))
            YES.Draw()
            NO.Draw()
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    run=False
                    force=True
                b1=NO.Detect(pygame.mouse.get_pos(),e)
                b2=YES.Detect(pygame.mouse.get_pos(),e)
                if b1:
                    run=False
                    val=False
                elif b2:
                    run=False
                    val=True
        if force:
            pygame.quit()
            return 'FORCE'
        else:
            pygame.quit()
            return val
                
                    