import View
import numpy as np
import Model
import tkFileDialog
from Tkinter import DISABLED, NORMAL
#from scipy.spatial import distance
import math

class Controller:
    def __init__(self):
        self.m=Model.Model()
        self.v=View.View(self)


    def angle_Change(self, value):
        self.m.angle_Camera=value#Borders checked at Tkinter Widget
        if(self.m.have_Object):
            self.set_Camera_Rectangle_Points()
            self.clear_Canvas()
            self.set_Canvas()


        #jesli sa punkty dla kamery to nalezy je zmienic, jezeli wyjda poza obszar kamery to nalez zmienic rozmiar,


    def Zoom_Top_Left_Plus(self):
        if(self.m.zoom_Canvas[0]==9):#Disable if max
            self.v.plus_Top_Left_Button['state']=DISABLED
            self.m.zoom_Canvas[0]+=1
        else:
            self.m.zoom_Canvas[0]+=1

        if(self.m.zoom_Canvas[0]>1):#Minus active if not 1
            self.v.minus_Top_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[0])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.set_Canvas()

    def Zoom_Top_Left_Minus(self):
        self.m.zoom_Canvas[0]-=1
        if(self.m.zoom_Canvas[0]==1):#Disable if min
            self.v.minus_Top_Left_Button['state']=DISABLED
        if(self.m.zoom_Canvas[0]<10):#Plus active if not 10
            self.v.plus_Top_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[0])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.set_Canvas()



    def Zoom_Top_Right_Plus(self):
        if(self.m.zoom_Canvas[1]==9):#Disable if max
            self.v.plus_Top_Right_Button['state']=DISABLED
            self.m.zoom_Canvas[1]+=1
        else:
            self.m.zoom_Canvas[1]+=1

        if(self.m.zoom_Canvas[1]>1):#Minus active if not 1
            self.v.minus_Top_Right_Button['state']=NORMAL
        print (self.m.zoom_Canvas[1])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.set_Canvas()

    def Zoom_Top_Right_Minus(self):
        self.m.zoom_Canvas[1]-=1
        if(self.m.zoom_Canvas[1]==1):#Disable if min
            self.v.minus_Top_Right_Button['state']=DISABLED
        if(self.m.zoom_Canvas[1]<10):#Plus active if not 10
            self.v.plus_Top_Right_Button['state']=NORMAL
        print (self.m.zoom_Canvas[1])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.set_Canvas()



    def Zoom_Bottom_Left_Plus(self):

        if(self.m.zoom_Canvas[2]==9):#Disable if max
            self.v.plus_Bottom_Left_Button['state']=DISABLED
            self.m.zoom_Canvas[2]+=1
        else:
            self.m.zoom_Canvas[2]+=1
        if(self.m.zoom_Canvas[2]>1):#Minus active if not 1
            self.v.minus_Bottom_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[2])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.set_Canvas()

    def Zoom_Bottom_Left_Minus(self):
        self.m.zoom_Canvas[2]-=1
        if(self.m.zoom_Canvas[2]==1):#Disable if min
            self.v.minus_Bottom_Left_Button['state']=DISABLED
        if(self.m.zoom_Canvas[2]<10):#Plus active if not 10
            self.v.plus_Bottom_Left_Button['state']=NORMAL
        print (self.m.zoom_Canvas[2])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.set_Canvas()

    def Open_Data(self):

        try:

            source=tkFileDialog.askdirectory()
            #####open model
            file=open(source+'/model.txt', 'r')

            #load vertices
            num_Verticles=int(file.readline())
            self.m.verticles= np.array([[int(i) for i in file.readline().strip('\n').split(',')] for i in range (0,num_Verticles)])

            #load numer of verticles in each triangle
            triangles_Number=int(file.readline())
            self.m.triangle_Verticles= tuple(tuple(int(i) for i in file.readline().strip('\n').split(',')) for i in range (0,triangles_Number))

            #load triangle color and surface parameters
            self.m.triangle_Color=[None]*triangles_Number
            self.m.triangle_Surface=[None] * triangles_Number
            for i in range(0,triangles_Number):
                temp=file.readline()
                elements=[int(s) for s in temp.strip('\n').split(' ')]
                self.m.triangle_Color[i], self.m.triangle_Surface[i]= tuple(elements[0:3]),tuple(elements[3:])
            self.m.triangle_Color=tuple(self.m.triangle_Color)
            self.m.triangle_Surface=tuple(self.m.triangle_Surface)

            #load light parameters
            temp=file.readline()
            elements= [int(s) for s in temp.strip('\n').split(' ')]
            self.m.light_Position, self.m.light_Color=  tuple(elements[0:3]),tuple(elements[3:])
            file.close()
            #####

            #####open camera
            file=open(source+'/kamera.txt','r')
            self.m.camera_Position=np.array([int(i) for i in file.readline().strip('\n').split(' ')])
            print  self.m.camera_Position

            self.m.viewport_Position=np.array([int(i) for i in file.readline().strip('\n').split(' ')])
            print self.m.viewport_Position

            self.m.angle_Camera=[int(i) for i in file.readline().strip('\n').split(' ')][0]
            #print self.m.angle_Camera
            file.close()
            #####
            self.v.angle_Camera.set(self.m.angle_Camera)
            self.m.have_Object=True

            self.clear_Canvas()

            self.set_Camera_Rectangle_Points()#checked good
            self.set_Centre_Scene1()#checked good
            self.set_Canvas()

        except :
            print 'IOException'





    def set_Camera_Rectangle_Points(self):
        temp_camera=self.m.camera_Position[:]
        temp_viewport=self.m.viewport_Position[:]
        dist=math.sqrt(pow(temp_camera[0]-temp_viewport[0],2)+pow(temp_camera[1]-temp_viewport[1],2)+pow(temp_camera[2]-temp_viewport[2],2))
        coord=math.tan(math.radians(float(self.m.angle_Camera/2)))*dist
        points=np.array([[coord ,coord, 0,1],
                        [coord,-coord, 0,1],
                        [-coord,-coord,0,1],
                        [-coord,coord,0,1]])
        self.m.camera_Rectangle_Points=np.transpose(np.dot(self.reverse_Camera_Matrix(),np.transpose(points)))


    def reverse_Camera_Matrix(self):
        #used to set rectangle points in right place in space
        temp_camera=self.m.camera_Position[:]
        temp_viewport=self.m.viewport_Position[:]
        angle=0
        if(temp_camera[2]==0):
            if(temp_camera[1]>0):
                angle=90
            elif(temp_camera[1]<0):
                angle=-90
            else:
                angle=0
        else:
            angle=-math.degrees(math.atan(temp_camera[1]/temp_camera[2]))
        rotateOX=self.rotation_X(angle)
        top=math.sqrt(pow(temp_camera[1],2) + pow(temp_camera[2],2))
        if(temp_camera[0]==0):
                angle=0
        else:
            angle=-math.degrees(  math.atan( temp_camera[0]/top  )  )
        rotateOY=self.rotation_Y(angle)
        translate=self.translation(temp_viewport[0],temp_viewport[1],temp_viewport[2])
        matrix=np.dot(rotateOX,rotateOY)
        return np.dot(translate,matrix)




    def translation(self,x,y,z):
        return np.array([[1 ,0 , 0,x],
                        [0 ,1 , 0,y],
                        [0,0,1,z],
                        [0,0,0,1]])

    def rotation_X(self,angle):
        return np.array([[1 ,0 , 0,0],
                        [0 ,math.cos(math.radians(angle)),-math.sin(math.radians(angle)),0],
                        [0,math.sin(math.radians(angle)),math.cos(math.radians(angle)),0],
                        [0,0,0,1]])

    def rotation_Y(self,angle):
        return np.array([[math.cos(math.radians(angle)) ,0 , math.sin(math.radians(angle)),0],
                        [0 ,1,0,0],
                        [-math.sin(math.radians(angle)),0,math.cos(math.radians(angle)),0],
                        [0,0,0,1]])

    def rotation_Z(self,angle):
        return np.array([[math.cos(math.radians(angle)) ,-math.sin(math.radians(angle)) ,0 ,0],
                        [math.sin(math.radians(angle)) ,math.cos(math.radians(angle)),0,0],
                        [0,0,1,0],
                        [0,0,0,1]])
    def scale_Matrix(self,times):
        return np.array([[times,0,0 ,0],
                        [0 ,times ,0,0],
                        [0,0,times,0],
                        [0,0,0,1]])
    def scale_Matrix2(self,x,y,z):
        return np.array([[x,0,0 ,0],
                        [0 ,y ,0,0],
                        [0,0,z,0],
                        [0,0,0,1]])

    def get_Canvas_Resolution(self):
        self.m.canvas_Resolution[0],self.m.canvas_Resolution[1]=self.v.canvas_Top_Left.winfo_width(),self.v.canvas_Top_Left.winfo_height()
        #print self.m.canvas_Resolution

    def prepare_Points_To_Show(self):
        """
        This function prepare all of our points to fit into Canvas'es.
        :return:
        """
        #zmiana rozmoaru bedzie miala miajsce tylko dla zmiany rozdzielczosci ekranu
        #points_Centre_Scene_View_Verticles=np.copy(self.m.verticles)
        #points_Centre_Scene_View_Camera=np.copy(self.m.camera_Position)
        #points_Centre_Scene_View_Viewpoint=np.copy(self.m.viewport_Position)
        #points_Centre_Scene_View_Rectangle=np.copy(self.m.camera_Rectangle_Points)

        if self.m.dispersion*2>min(self.m.canvas_Resolution):
            #self.m.prescaler=self.m.dispersion*2/min(self.m.canvas_Resolution)
            self.m.prescaler=min(self.m.canvas_Resolution)/(self.m.dispersion*2)
        else:
            self.m.prescaler=1.
       # print 'dispersion'
       # print self.m.dispersion
       # print 'resolution'
       # print self.m.canvas_Resolution
       # print 'prescaler'
        #print self.m.prescaler
       # print 'w srodku prescalera'
        self.prepare_Top_Left_Points()
        self.prepare_Bottom_Left_Points()
        self.prepare_Top_Right_Points()

       # print zoom
       # translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler)))
      #  print 'macierz translacji stara'
       # print translation
      #  prescale_Matrix=self.scale_Matrix(self.m.prescaler)
      #  print 'macierz skalowania stara'
      #  print prescale_Matrix
        #najpierw transpozycja i pozniej zmniejszanie
        #czy najpierw zmniejszanie a pozniej ta dziwna transpozycja
        #prescale all scene


     #   points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(points_Centre_Scene_View_Verticles))
      #  points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(points_Centre_Scene_View_Camera))
      #  points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(points_Centre_Scene_View_Viewpoint))
      #  points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(points_Centre_Scene_View_Rectangle))
        #move axis to centre of scene
     #   points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
     #   points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
      #  points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
      #  points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)

        #to ponizej wyglada git i to co jest pozniej
        #cos nie gra z prescalerem
        #How translations whould be corrected:(all points fit into canvas(plus values))
        #yox Y-1/2 HEIGHT X 1/2 WIDTH
        #zox Z-1/2 HEIGHT X 1/2 WIDTH
        #0-width 1-height
      #  translation_Left_Canvas=self.translation(self.m.canvas_Resolution[0]/2., self.m.canvas_Resolution[1]/2., self.m.canvas_Resolution[1]/2.)
      #  self.m.Top_Left_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
     #   self.m.Top_Left_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
      #  self.m.Top_Left_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
      #  self.m.Top_Left_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)


        #zoy z-1/2 WIDTH y 1/2 Height
       # translation_Top_Right_Canvas=self.translation(self.m.canvas_Resolution[0]/2., self.m.canvas_Resolution[1]/2., self.m.canvas_Resolution[0]/2.)
      #  self.m.Top_Right_Canvas_Verticles=np.dot(translation_Top_Right_Canvas, points_Centre_Scene_View_Verticles)
       # self.m.Top_Right_Canvas_Camera=np.dot(translation_Top_Right_Canvas, points_Centre_Scene_View_Camera)
       # self.m.Top_Right_Canvas_Viewpoint=np.dot(translation_Top_Right_Canvas, points_Centre_Scene_View_Viewpoint)
       # self.m.Top_Right_Canvas_Rectangle=np.dot(translation_Top_Right_Canvas, points_Centre_Scene_View_Rectangle)


    def prepare_Bottom_Left_Points(self):

        zoom= (self.m.zoom_Canvas[2]/10.)
        translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler*zoom)))

        prescale_Matrix=self.scale_Matrix(self.m.prescaler*zoom)
        points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(self.m.verticles))
        points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(self.m.camera_Position))
        points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(self.m.viewport_Position))
        points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(self.m.camera_Rectangle_Points))
        #Move axis to centre of scene
        points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
        points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
        points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
        points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)
        #Adjust scene to resolution of canvas
        translation_Left_Canvas=self.translation(self.m.canvas_Resolution[0]/2., 0,self.m.canvas_Resolution[1]/2.)
        self.m.Bottom_Left_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
        self.m.Bottom_Left_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
        self.m.Bottom_Left_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
        self.m.Bottom_Left_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)

    def prepare_Top_Left_Points(self):
        #points_Centre_Scene_View_Verticles=np.copy(self.m.verticles)
        #points_Centre_Scene_View_Camera=np.copy(self.m.camera_Position)
        #points_Centre_Scene_View_Viewpoint=np.copy(self.m.viewport_Position)
        #points_Centre_Scene_View_Rectangle=np.copy(self.m.camera_Rectangle_Points)

        zoom= self.m.zoom_Canvas[0]/10.
        translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler*zoom)))
        prescale_Matrix=self.scale_Matrix(self.m.prescaler*zoom)

        points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(self.m.verticles))
        points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(self.m.camera_Position))
        points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(self.m.viewport_Position))
        points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(self.m.camera_Rectangle_Points))
        #Move axis to centre of scene
        points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
        points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
        points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
        points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)
        #Adjust scene to resolution of canvas
        translation_Left_Canvas=self.translation(self.m.canvas_Resolution[0]/2., self.m.canvas_Resolution[1]/2.,0)
        self.m.Top_Left_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
        self.m.Top_Left_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
        self.m.Top_Left_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
        self.m.Top_Left_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)

    def prepare_Top_Right_Points(self):
        zoom= self.m.zoom_Canvas[1]/10.
        translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler*zoom)))
        prescale_Matrix=self.scale_Matrix(self.m.prescaler*zoom)
        points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(self.m.verticles))
        points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(self.m.camera_Position))
        points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(self.m.viewport_Position))
        points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(self.m.camera_Rectangle_Points))
        #Move axis to centre of scene
        points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
        points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
        points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
        points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)
        #Adjust scene to resolution of canvas
        translation_Left_Canvas=self.translation(0, self.m.canvas_Resolution[1]/2., self.m.canvas_Resolution[0]/2.)
        self.m.Top_Right_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
        self.m.Top_Right_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
        self.m.Top_Right_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
        self.m.Top_Right_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)


    def set_Canvas(self):
        #pobranie wszystkich danych i przemielenie ich w podrecznym buforze tak aby mozna go bylu zrzutowac na wszystkie
        #dla zmian punktow, dla zmian rozdzielczosc, dla zmian katow

        self.get_Canvas_Resolution()
        self.prepare_Points_To_Show()
        self.Draw_Camera_Triangle()
        self.Refresh_Top_Left_Canvas()
        self.Refresh_Top_Right_Canvas()
        self.Refresh_Bottom_Left_Canvas()
        self.Refresh_Bottom_Right_Canvas()




    def set_Centre_Scene1(self):
        #get sum of camera and object and then find centre point

        sum_Object=np.sum(self.m.verticles,axis=0)
        sum_Object=sum_Object/sum_Object[3]
        sum_Camera=(self.m.viewport_Position+self.m.camera_Position)/2
        self.m.centre_World_Scene=(sum_Object+sum_Camera)/2

        dispersion=0
        #calculate distance between verticles and calculated centre
        for i in range(0,self.m.verticles.shape[0]):
            temp=math.sqrt(pow(self.m.centre_World_Scene[0]-self.m.verticles[i][0],2)+pow(self.m.centre_World_Scene[1]-self.m.verticles[i][1],2)+pow(self.m.centre_World_Scene[2]-self.m.verticles[i][2],2))
            if temp>dispersion:dispersion=temp

        #caltulace distance between camera and calculated centre
        temp=math.sqrt(pow(self.m.centre_World_Scene[0]-self.m.camera_Position[0],2)+pow(self.m.centre_World_Scene[1]-self.m.camera_Position[1],2)+pow(self.m.centre_World_Scene[2]-self.m.camera_Position[2],2))
        if temp>dispersion:dispersion=temp

        #calculate distance between viewport and calculated scene
        temp=math.sqrt(pow(self.m.centre_World_Scene[0]-self.m.viewport_Position[0],2)+pow(self.m.centre_World_Scene[1]-self.m.viewport_Position[1],2)+pow(self.m.centre_World_Scene[2]-self.m.viewport_Position[2],2))
        if temp>dispersion:dispersion=temp

        #calculate distence between caamera rectangle points and calculated scene
        for i in range(0,self.m.camera_Rectangle_Points.shape[0]):
            temp=math.sqrt(pow(self.m.centre_World_Scene[0]-self.m.camera_Rectangle_Points[i][0],2)+pow(self.m.centre_World_Scene[1]-self.m.camera_Rectangle_Points[i][1],2)+pow(self.m.centre_World_Scene[2]-self.m.camera_Rectangle_Points[i][2],2))
            if temp>dispersion:dispersion=temp

        self.m.dispersion=dispersion




    def Refresh_Top_Left_Canvas(self):
        #tworzymy reprezentacje punktow w macierzy NUMPY i wrzucamy to jako obraz do CANVASU
        to_Canvas_View=np.dot(self.translation(0,self.m.canvas_Resolution[1],0),self.scale_Matrix2(1,-1,1))
        verticles=np.dot(to_Canvas_View,self.m.Top_Left_Canvas_Verticles)
        for i in self.m.triangle_Verticles:
            for j in range(-1,2):
                self.v.canvas_Top_Left.create_line(verticles[0][i[j]],verticles[1][i[j]],verticles[0][i[j+1]],verticles[1][i[j+1]])

    def Refresh_Top_Right_Canvas(self):
        #tworzymy reprezentacje punktow w macierzy NUMPY i wrzucamy to jako obraz do CANVASU
        to_Canvas_View=np.dot(self.translation(0,self.m.canvas_Resolution[1],0),self.scale_Matrix2(1,-1,1))
        verticles=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Verticles)
       # print 'verticles'
        #print verticles
        #print 'points'
        ##chwilowe rozwiazanie by sprawdzic jak wyglada to wszystko po przeksztalceniach
        print  len(self.m.triangle_Verticles)
        for i in self.m.triangle_Verticles:
            for j in range(-1,2):
                #i[j] indeks pierwszego wierzcholka i[j+1] indeks drugiego wierzcholka
                pass
                self.v.canvas_Top_Right.create_line(verticles[2][i[j]],verticles[1][i[j]],verticles[2][i[j+1]],verticles[1][i[j+1]])

    def Refresh_Bottom_Left_Canvas(self):

        #tworzymy reprezentacje punktow w macierzy NUMPY i wrzucamy to jako obraz do CANVASU
        to_Canvas_View=np.dot(self.translation(0,0,self.m.canvas_Resolution[1]),self.scale_Matrix2(1,1,-1))
        verticles=np.dot(to_Canvas_View,self.m.Bottom_Left_Canvas_Verticles)
       # print 'verticles'
        #print verticles
        #print 'points'
        ##chwilowe rozwiazanie by sprawdzic jak wyglada to wszystko po przeksztalceniach
        print  len(self.m.triangle_Verticles)
        for i in self.m.triangle_Verticles:
            for j in range(-1,2):
                #i[j] indeks pierwszego wierzcholka i[j+1] indeks drugiego wierzcholka
                pass
                self.v.canvas_Bottom_Left.create_line(verticles[0][i[j]],verticles[2][i[j]],verticles[0][i[j+1]],verticles[2][i[j+1]])

    def Refresh_Bottom_Right_Canvas(self):
        pass

    def Normalize_Matrix(self):
        pass

    def Draw_Camera_Triangle(self):
        #mozna pomyslec nad rozdzieleniem do poszczegolnych canvasow tych przeksztalcen
        to_Canvas_View=np.dot(self.translation(0,self.m.canvas_Resolution[1],self.m.canvas_Resolution[1]),self.scale_Matrix2(1,-1,-1))
        self.Draw_Top_Left_Camera_Triangle(to_Canvas_View)
        self.Draw_Bottom_Left_Camera_Triangle(to_Canvas_View)

    #    camera=np.dot(to_Canvas_View,self.m.Left_Canvas_Camera)
     #   viewport=np.dot(to_Canvas_View,self.m.Left_Canvas_Viewpoint)
     #   points=np.dot(to_Canvas_View,self.m.Left_Canvas_Rectangle)

        #TOP LEFT CANVAS
      #  for i in range(0,4):
      #      self.v.canvas_Top_Left.create_line(camera[0],camera[1],points[0][i],points[1][i])
      #  self.v.canvas_Top_Left.create_line(camera[0],camera[1], viewport[0], viewport[1],fill='red', width=3 )
      #  for i in range(-1,3):
       #     self.v.canvas_Top_Left.create_line(points[0][i],points[1][i],points[0][i+1],points[1][i+1])
#
 #       #BOTTOM LEFT
  #      for i in range(0,4):
   #         self.v.canvas_Bottom_Left.create_line(camera[0],camera[2],points[0][i],points[2][i])
    #    self.v.canvas_Bottom_Left.create_line(camera[0],camera[2], viewport[0], viewport[2],fill='red', width=3 )
     #   for i in range(-1,3):
      #      self.v.canvas_Bottom_Left.create_line(points[0][i],points[2][i],points[0][i+1],points[2][i+1])


        to_Canvas_View=np.dot(self.translation(0,self.m.canvas_Resolution[1],0),self.scale_Matrix2(1,-1,1))
        self.Draw_Top_Right_Camera_Triangle(to_Canvas_View)
     #   camera=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Camera)
     #  viewport=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Viewpoint)
      #  points=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Rectangle)

        #TOP RIGHT
      #  for i in range(0,4):
     #       self.v.canvas_Top_Right.create_line(camera[2],camera[1],points[2][i],points[1][i])
     #   self.v.canvas_Top_Right.create_line(camera[2],camera[1], viewport[2], viewport[1],fill='red', width=3 )
     #   for i in range(-1,3):
     #       self.v.canvas_Top_Right.create_line(points[2][i],points[1][i],points[2][i+1],points[1][i+1])

    def Draw_Bottom_Left_Camera_Triangle(self,matrix):
        camera=np.dot(matrix,self.m.Bottom_Left_Canvas_Camera)
        viewport=np.dot(matrix,self.m.Bottom_Left_Canvas_Viewpoint)
        points=np.dot(matrix,self.m.Bottom_Left_Canvas_Rectangle)

        self.m.clickable_Points['Bottom_Left_Camera']=camera
        self.m.clickable_Points['Bottom_Left_Viewpoint']=viewport

        for i in range(0,4):
            self.v.canvas_Bottom_Left.create_line(camera[0],camera[2],points[0][i],points[2][i])
        self.v.canvas_Bottom_Left.create_line(camera[0],camera[2], viewport[0], viewport[2],fill='red', width=3 )
        for i in range(-1,3):
            self.v.canvas_Bottom_Left.create_line(points[0][i],points[2][i],points[0][i+1],points[2][i+1])

    def Draw_Top_Left_Camera_Triangle(self, matrix):
        camera=np.dot(matrix,self.m.Top_Left_Canvas_Camera)
        viewport=np.dot(matrix,self.m.Top_Left_Canvas_Viewpoint)
        points=np.dot(matrix,self.m.Top_Left_Canvas_Rectangle)

        self.m.clickable_Points['Top_Left_Camera']=camera
        self.m.clickable_Points['Top_Left_Viewpoint']=viewport

        for i in range(0,4):
            self.v.canvas_Top_Left.create_line(camera[0],camera[1],points[0][i],points[1][i])
        self.v.canvas_Top_Left.create_line(camera[0],camera[1], viewport[0], viewport[1],fill='red', width=3 )
        for i in range(-1,3):
            self.v.canvas_Top_Left.create_line(points[0][i],points[1][i],points[0][i+1],points[1][i+1])

    def Draw_Top_Right_Camera_Triangle(self,matrix):
        camera=np.dot(matrix,self.m.Top_Right_Canvas_Camera)
        viewport=np.dot(matrix,self.m.Top_Right_Canvas_Viewpoint)
        points=np.dot(matrix,self.m.Top_Right_Canvas_Rectangle)

        self.m.clickable_Points['Top_Right_Camera']=camera
        self.m.clickable_Points['Top_Right_Viewpoint']=viewport

        for i in range(0,4):
            self.v.canvas_Top_Right.create_line(camera[2],camera[1],points[2][i],points[1][i])
        self.v.canvas_Top_Right.create_line(camera[2],camera[1], viewport[2], viewport[1],fill='red', width=3 )
        for i in range(-1,3):
            self.v.canvas_Top_Right.create_line(points[2][i],points[1][i],points[2][i+1],points[1][i+1])


    def clear_Canvas(self):
        self.v.canvas_Top_Right.delete('all')
        self.v.canvas_Top_Left.delete('all')
        self.v.canvas_Bottom_Left.delete('all')


if __name__=='__main__':
    c=Controller()
    c.v.Start_App()

