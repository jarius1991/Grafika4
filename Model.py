import numpy as np

class Model:

    def __init__(self):
        #self.angle_Camera
        self.camera_Position=np.matrix('0;0;0;1')
        self.viewport_Position=np.matrix('0;0;10;1')
        self.angle_Camera=1
        self.camera_Rectangle_Points=[0,0,0,0]

        self.matrix_Projection_TopLeftCanvas=np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 0; 0 0 0 1")
        self.matrix_Projection_TopRightCanvas=np.matrix("1 0 0 0; 0 0 0 0; 0 0 1 0; 0 0 0 1")
        self.matrix_Projection_BotLeftCanvas=np.matrix("0 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1")

        #0-Top_Left, 1-Top_Right, 2-Bottom_Left
        self.zoom_Canvas=[2,2,2]#1-min 10-max


        self.centre_World_Scene=(0,0,0)# not necessary
        #jak bardzo sa rozjebane elementy
        #rozmiar okna definiuje jak ma byc umieszczana scena cala
        self.canvas_Resolution=[100,100]



        print np.dot(self.matrix_Projection_TopLeftCanvas, self.camera_Position)






