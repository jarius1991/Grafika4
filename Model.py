import numpy as np

class Model:
#zebrac wszystkie dane i je tutaj ladnie uporzadkowac
    def __init__(self):
        #self.angle_Camera
        self.camera_Position=np.matrix('0;0;0;1')
        self.viewport_Position=np.matrix('0;0;10;1')
        self.angle_Camera=1
        self.camera_Rectangle_Points= np.matrix('0 0 0 1;0 0 0 1;0 0 0 1;0 0 0 1')



        self.matrix_Projection_TopLeftCanvas=np.matrix("1 0 0 0; 0 1 0 0; 0 0 0 0; 0 0 0 1")
        self.matrix_Projection_TopRightCanvas=np.matrix("1 0 0 0; 0 0 0 0; 0 0 1 0; 0 0 0 1")
        self.matrix_Projection_BotLeftCanvas=np.matrix("0 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1")

        #0-Top_Left, 1-Top_Right, 2-Bottom_Left
        self.zoom_Canvas=[10,10,10]#1-min 10-max


        self.centre_World_Scene=np.array([0,0,0,0])# not necessary
        self.dispersion=0
        #jak bardzo sa rozjebane elementy
        #rozmiar okna definiuje jak ma byc umieszczana scena cala
        self.canvas_Resolution=[100,100]

        self.triangle_Color=[]
        self.triangle_Surface=[]
        self.have_Object= False
        #print np.dot(self.matrix_Projection_TopLeftCanvas, self.camera_Position)
        self.clickable_Points={'Top_Left_Camera':None,
                               'Top_Left_Viewpoint':None,
                               'Top_Right_Camera':None,
                               'Top_Right_Viewpoint':None,
                               'Bottom_Left_Camera':None,
                               'Bottom_Left_Viewpoint':None}
        self.point_Clicked_Canvas=[0,0]
        self.clicked_Point_Position={}

        self.top_Left_Background=None
        self.top_Left_Depth=None

        self.top_Right_Background=None
        self.top_Right_Depth=None

        self.bottom_Left_Background=None
        self.bottom_Left_Depth=None
        self.triangle_Normals={}
        self.triangle_Planes={}
        self.verticle_Normals={}






