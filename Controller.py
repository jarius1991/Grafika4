import View
import numpy as np
import Model

class Controller:
    def __init__(self):
        self.m=Model.Model()
        self.v=View.View(self)


    def angle_Change(self, value):
        self.m.angle_Camera=value
        #print value

    def costam(self):
        pass









if __name__=='__main__':
    c=Controller()
    c.v.Start_App()

