class Draw:
    def __init__(self,**kwarg):
        self.Draws=[]
        for key,val in kwarg.items():
            self.Draws.append(val)
    def Draw_All(self):
        for thing in self.Draws:
            thing.Draw()
    def Add_Item(self,Item):
        self.Draw.append(Item)
class Simple_Blit:
    def __init__(self,screen,**kwarg):
        self.blits=[]
        self.screen=screen
        for key,val in kwarg.items():
            self.blits.append(val)
    def Draw_All(self):
        item=[]
        for thing in self.blits:
            for more in thing:
                item.append(item)
            self.screen.blit(item[0],(item[1],item[2]))
            item=[]
    def Add_Item(self,Item):
        self.blits.append(Item)