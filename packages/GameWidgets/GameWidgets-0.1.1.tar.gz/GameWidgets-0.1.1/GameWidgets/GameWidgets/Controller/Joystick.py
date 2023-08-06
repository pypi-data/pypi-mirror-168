import pygame
class JoyStick:
    def __init__(self,screen):
        pygame.joystick.init()
        self.screen=screen
        self.joystick_count=pygame.joystick.get_count()
    def Joystick_Type(self):
        return self.joystick.get_name()
    def Return_Joystick(self):
        FullList=[]
        for i in range(self.joystick_count):
            joystick=pygame.joystick.Joystick(i)
            joystick.init()
            FullList.append(joystick)
        return FullList
    def Get_Axis(self,Nums=(0,0),Return=False):
        for i in range(self.joystick_count):
            joystick=pygame.joystick.Joystick(i)
            joystick.init()
            axis = joystick.get_numaxes()
            for i in range(axis):
                stick=joystick.get_axis(i)
                if i==Nums[0]:
                    if Return:
                        return stick
                    else:
                        if stick!=float(-1):
                            return {i:stick}
                        else:
                            return (0,0)
                elif i==Nums[1]:
                    if Return:
                        return stick
                    else:
                        if stick!=float(-1):
                            return {i:stick}
                        else:
                            return (0,0)
                else:
                    return {100:'False'}