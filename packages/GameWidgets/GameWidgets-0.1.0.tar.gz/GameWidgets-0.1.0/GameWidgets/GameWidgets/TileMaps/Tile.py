def Draw(Surface,KEY={},MAP='''''',TILESIZE=(10,10),START_POS=(0,0),MAX=(400,400)):
        x=START_POS[0]
        y=START_POS[1]
        for item in MAP:
            for key in KEY.keys():
                if key==item:
                    Surface.blit(KEY[key],(x,y))
                    
                    if x<MAX[0]:
                        x+=TILESIZE[0]
                        #print(x," : ",y)
                    else:
                        if y<MAX[1]:
                            y+=TILESIZE[1]
                            x=START_POS[0]
                        else:
                            pass
            if item=='n':
                y+=TILESIZE[1]
                x=START_POS[0]