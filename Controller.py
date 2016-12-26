import View
import numpy as np
import Model
from Tkinter import DISABLED, NORMAL

class Controller:
    def __init__(self):
        self.m=Model.Model()
        self.v=View.View(self)


    def angle_Change(self, value):
        self.m.angle_Camera=value#Borders checked at Canvas Widget


    def Zoom_Top_Left_Plus(self):
        self.m.zoom_Canvas[0]+=1
        if(self.m.zoom_Canvas[0]==10):#Disable if max
            self.v.plus_Top_Left_Button['state']=DISABLED
        if(self.m.zoom_Canvas[0]>1):#Minus active if not 1
            self.v.minus_Top_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[0])

    def Zoom_Top_Left_Minus(self):
        self.m.zoom_Canvas[0]-=1
        if(self.m.zoom_Canvas[0]==1):#Disable if min
            self.v.minus_Top_Left_Button['state']=DISABLED
        if(self.m.zoom_Canvas[0]<10):#Plus active if not 10
            self.v.plus_Top_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[0])




    def Zoom_Top_Right_Plus(self):
        self.m.zoom_Canvas[1]+=1
        if(self.m.zoom_Canvas[1]==10):#Disable if max
            self.v.plus_Top_Right_Button['state']=DISABLED
        if(self.m.zoom_Canvas[1]>1):#Minus active if not 1
            self.v.minus_Top_Right_Button['state']=NORMAL
        print (self.m.zoom_Canvas[1])

    def Zoom_Top_Right_Minus(self):
        self.m.zoom_Canvas[1]-=1
        if(self.m.zoom_Canvas[1]==1):#Disable if min
            self.v.minus_Top_Right_Button['state']=DISABLED
        if(self.m.zoom_Canvas[1]<10):#Plus active if not 10
            self.v.plus_Top_Right_Button['state']=NORMAL
        print (self.m.zoom_Canvas[1])



    def Zoom_Bottom_Left_Plus(self):
        self.m.zoom_Canvas[2]+=1
        if(self.m.zoom_Canvas[2]==10):#Disable if max
            self.v.plus_Bottom_Left_Button['state']=DISABLED
        if(self.m.zoom_Canvas[2]>1):#Minus active if not 1
            self.v.minus_Bottom_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[2])

    def Zoom_Bottom_Left_Minus(self):
        self.m.zoom_Canvas[2]-=1
        if(self.m.zoom_Canvas[2]==1):#Disable if min
            self.v.minus_Bottom_Left_Button['state']=DISABLED
        if(self.m.zoom_Canvas[2]<10):#Plus active if not 10
            self.v.plus_Bottom_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[2])








if __name__=='__main__':
    c=Controller()
    c.v.Start_App()

