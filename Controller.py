from __future__ import division
import View
import numpy as np
import Model
import tkFileDialog
from Tkinter import DISABLED, NORMAL
#from scipy.spatial import distance
import math
from PIL import  Image,ImageTk,ImageOps

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
            self.m.Resize_Top_Left=True
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
            self.m.Resize_Top_Left=True
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
            self.m.Resize_Top_Right=True
            self.set_Canvas()

    def Zoom_Top_Right_Minus(self):
        self.m.zoom_Canvas[1]-=1
        if(self.m.zoom_Canvas[1]==1):#Disable if min
            self.v.minus_Top_Right_Button['state']=DISABLED
        if(self.m.zoom_Canvas[1]<10):#Plus active if not 10
            self.v.plus_Top_Right_Button['state']=NORMAL
        #print (self.m.zoom_Canvas[1])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.m.Resize_Top_Right=True
            self.set_Canvas()



    def Zoom_Bottom_Left_Plus(self):

        if(self.m.zoom_Canvas[2]==9):#Disable if max
            self.v.plus_Bottom_Left_Button['state']=DISABLED
            self.m.zoom_Canvas[2]+=1
        else:
            self.m.zoom_Canvas[2]+=1
        if(self.m.zoom_Canvas[2]>1):#Minus active if not 1
            self.v.minus_Bottom_Left_Button['state']=NORMAL
        #print (self.m.zoom_Canvas[2])
        if(self.m.have_Object):
            self.clear_Canvas()
            self.m.Resize_Bottom_Left=True
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
            self.Refresh_Bottom_Left_Canvas()
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
            self.m.light_Position, self.m.light_Color=  tuple(elements[0:4]),tuple(elements[4:])
            file.close()
            #####

            #####open camera
            file=open(source+'/kamera.txt','r')
            self.m.camera_Position=np.array([int(i) for i in file.readline().strip('\n').split(' ')])
            #print  self.m.camera_Position

            self.m.viewport_Position=np.array([int(i) for i in file.readline().strip('\n').split(' ')])
            #print self.m.viewport_Position

            self.m.angle_Camera=[int(i) for i in file.readline().strip('\n').split(' ')][0]
            #print self.m.angle_Camera
            file.close()
            #####
            self.v.angle_Camera.set(self.m.angle_Camera)
            self.m.have_Object=True
            self.clear_Canvas()
            self.m.Refresh_Background=True
            self.m.Refresh_Camera_View=True
         # np w tym miejscu powinnismy obliczyc normalne
            self.Prepare_Normal_Vectors()
            self.set_Camera_Rectangle_Points()#checked good
            self.set_Centre_Scene1()#checked good
            self.set_Canvas()

        except Exception as e:
            print 'Exception'
            #Image.fromarray(self.m.top_Right_Background,'RGB').show()
            #print e




    def Prepare_Normal_Vectors(self):
        self.m.triangle_Normals=np.zeros((len(self.m.triangle_Verticles),3))
        #print 'zmieniamy normalne', self.m.triangle_Normals
        for triangle_nr in range(0,len(self.m.triangle_Verticles)):
            triangle=self.m.triangle_Verticles[triangle_nr]
            #print triangle
            verticles= np.transpose( self.m.verticles)
            points=(verticles[0:3,triangle[0]],verticles[0:3,triangle[1]],verticles[0:3,triangle[2]])
            self.m.triangle_Normals[triangle_nr]=self.Count_Normal_Vector(points)
        #print 'zmieniamy normalne//po zainicjowaniu', self.m.triangle_Normals



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
        print self.m.camera_Rectangle_Points



    def reverse_Camera_Matrix(self):
        #used to set rectangle points in right place in space
        temp_camera=self.m.camera_Position.copy()
        temp_viewport=self.m.viewport_Position.copy()
        angle=0
        if(temp_camera[2]==0):
            if(temp_camera[1]>0):
                angle=90
            elif(temp_camera[1]<0):
                angle=-90
            else:
                angle=0
        else:

            #print 'test: ',  float(temp_camera[1])/temp_camera[2]
            angle=-math.degrees(math.atan(float(temp_camera[1])/temp_camera[2]))#w code review doogarnac dzielenie
    #rotation OX
        rotateOX=self.rotation_X(angle)
        rotateOX_toCompute=self.rotation_X(-angle)
        top=math.sqrt(pow(temp_camera[1],2) + pow(temp_camera[2],2))
        #print top
        if(temp_camera[0]==0):
            angle=0
        else:
            angle=-math.degrees(  math.atan( float(temp_camera[0])/top  )  )

    #rotation OY
        rotateOY=self.rotation_Y(angle)
        rotateOY_toCompute=self.rotation_Y(-angle)
        translate=self.translation(temp_viewport[0],temp_viewport[1],temp_viewport[2])

        matrix_toCompute=np.dot(rotateOY_toCompute,rotateOX_toCompute)

        Y=np.array([[0],[1],[0],[1]])
        Y= np.dot(matrix_toCompute,Y)

        angle=-math.degrees(math.atan(float(Y[0])/Y[1]))#w code review doogarnac dzielenie
        rotateOZ=self.rotation_Z(angle)
        matrix=np.dot(rotateOY,rotateOZ)
        matrix=np.dot(rotateOX,matrix)
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

    def prepare_Points_To_Show(self):
        if self.m.dispersion*2>min(self.m.canvas_Resolution):
            #self.m.prescaler=self.m.dispersion*2/min(self.m.canvas_Resolution)
            self.m.prescaler=min(self.m.canvas_Resolution)/(self.m.dispersion*2)
        else:
            self.m.prescaler=1.
        self.prepare_Top_Left_Points()
        self.prepare_Bottom_Left_Points()
        self.prepare_Top_Right_Points()


    def prepare_Bottom_Left_Points(self):

        zoom= (self.m.zoom_Canvas[2]/10.)
        translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler*zoom)))
        prescale_Matrix=self.scale_Matrix(self.m.prescaler*zoom)

        points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(self.m.verticles))
        points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(self.m.camera_Position))
        points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(self.m.viewport_Position))
        points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(self.m.camera_Rectangle_Points))
        points_Centre_Scene_View_Light=np.dot(prescale_Matrix,np.transpose(self.m.light_Position))
        #Move axis to centre of scene
        points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
        points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
        points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
        points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)
        points_Centre_Scene_View_Light=np.dot(translation,points_Centre_Scene_View_Light)
        #Adjust scene to resolution of canvas
        translation_Left_Canvas=self.translation(self.m.canvas_Resolution[0]/2., 0,self.m.canvas_Resolution[1]/2.)
        self.m.Bottom_Left_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
        self.m.Bottom_Left_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
        self.m.Bottom_Left_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
        self.m.Bottom_Left_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)
        self.m.Bottom_Left_Canvas_Light=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Light)


    def prepare_Top_Left_Points(self):
        zoom= self.m.zoom_Canvas[0]/10.
        translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler*zoom)))
        prescale_Matrix=self.scale_Matrix(self.m.prescaler*zoom)

        points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(self.m.verticles))
        points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(self.m.camera_Position))
        points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(self.m.viewport_Position))
        points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(self.m.camera_Rectangle_Points))
        points_Centre_Scene_View_Light=np.dot(prescale_Matrix,np.transpose(self.m.light_Position))
        #Move axis to centre of scene
        points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
        points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
        points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
        points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)
        points_Centre_Scene_View_Light=np.dot(translation,points_Centre_Scene_View_Light)
        #Adjust scene to resolution of canvas
        translation_Left_Canvas=self.translation(self.m.canvas_Resolution[0]/2., self.m.canvas_Resolution[1]/2.,0)
        self.m.Top_Left_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
        self.m.Top_Left_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
        self.m.Top_Left_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
        self.m.Top_Left_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)
        self.m.Top_Left_Canvas_Light=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Light)

    def prepare_Top_Right_Points(self):
        zoom= self.m.zoom_Canvas[1]/10.
        translation=self.translation(*(self.m.centre_World_Scene[:3]*(-self.m.prescaler*zoom)))
        prescale_Matrix=self.scale_Matrix(self.m.prescaler*zoom)

        points_Centre_Scene_View_Verticles=np.dot(prescale_Matrix,np.transpose(self.m.verticles))
        points_Centre_Scene_View_Camera=np.dot(prescale_Matrix,np.transpose(self.m.camera_Position))
        points_Centre_Scene_View_Viewpoint=np.dot(prescale_Matrix,np.transpose(self.m.viewport_Position))
        points_Centre_Scene_View_Rectangle=np.dot(prescale_Matrix,np.transpose(self.m.camera_Rectangle_Points))
        points_Centre_Scene_View_Light=np.dot(prescale_Matrix,np.transpose(self.m.light_Position))
        #Move axis to centre of scene
        points_Centre_Scene_View_Verticles=np.dot(translation,points_Centre_Scene_View_Verticles)
        points_Centre_Scene_View_Camera=np.dot(translation,points_Centre_Scene_View_Camera)
        points_Centre_Scene_View_Viewpoint=np.dot(translation,points_Centre_Scene_View_Viewpoint)
        points_Centre_Scene_View_Rectangle=np.dot(translation,points_Centre_Scene_View_Rectangle)
        points_Centre_Scene_View_Light=np.dot(translation,points_Centre_Scene_View_Light)
        #Adjust scene to resolution of canvas
        translation_Left_Canvas=self.translation(0, self.m.canvas_Resolution[1]/2., self.m.canvas_Resolution[0]/2.)
        self.m.Top_Right_Canvas_Verticles=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Verticles)
        self.m.Top_Right_Canvas_Camera=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Camera)
        self.m.Top_Right_Canvas_Viewpoint=np.dot(translation_Left_Canvas, points_Centre_Scene_View_Viewpoint)
        self.m.Top_Right_Canvas_Rectangle=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Rectangle)
        self.m.Top_Right_Canvas_Light=np.dot(translation_Left_Canvas,points_Centre_Scene_View_Light)

    def set_Canvas(self):
        self.get_Canvas_Resolution()
        self.prepare_Points_To_Show()
        self.Draw_Camera_Triangle()
        if(self.m.Refresh_Background):
            self.Refresh_Top_Left_Canvas()
            self.Refresh_Top_Right_Canvas()
            self.Refresh_Bottom_Left_Canvas()
            self.m.Refresh_Background=False
        else:
            if self.m.Resize_Top_Left:
                self.Refresh_Top_Left_Canvas()
                self.m.Resize_Top_Left=False
            if self.m.Resize_Top_Right:
                self.Refresh_Top_Right_Canvas()
                self.m.Resize_Top_Right=False
            if self.m.Resize_Bottom_Left:
                self.m.Resize_Bottom_Left
                self.m.Resize_Bottom_Left=False

            self.Set_Top_Left_Canvas()
            self.Set_Top_Right_Canvas()
            self.Set_Bottom_Left_Canvas()
            self.Set_Bottom_Right_Canvas()

            #funkcje tylko wstawiajace obliczony background
        if(self.m.Refresh_Camera_View):
            self.Refresh_Bottom_Right_Canvas()
            #tutaj wstaw funkcje odswierzajaca czwarte okno
            self.m.Refresh_Camera_View=False




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
        to_Canvas_View=np.dot(self.translation(0,self.m.canvas_Resolution[1],0),self.scale_Matrix2(1,-1,1))
        verticles=np.dot(to_Canvas_View,self.m.Top_Left_Canvas_Verticles)
        light=np.dot(to_Canvas_View,self.m.Top_Left_Canvas_Light)
        camera=np.dot(to_Canvas_View,self.m.Top_Left_Canvas_Camera)
        normal= self.m.triangle_Normals.copy()
        normal[:,1]=-normal[:,1]

        background=self.Generate_Top_Left_Canvas_Background(verticles, normal, light, camera)

        id=self.Set_Top_Left_Canvas()

        #for i in self.m.triangle_Verticles:
         #   for j in range(-1,2):
          #      self.v.canvas_Top_Left.create_line(verticles[0][i[j]],verticles[1][i[j]],verticles[0][i[j+1]],verticles[1][i[j+1]])

    def Set_Top_Left_Canvas(self):
        image2 = Image.fromarray(self.m.top_Left_Background,'RGB')
        self.image_TK_TL = ImageTk.PhotoImage(image2)
        id=self.v.canvas_Top_Left.create_image(self.m.canvas_Resolution[0]/2, self.m.canvas_Resolution[1]/2, image=self.image_TK_TL)
        self.v.canvas_Top_Left.lower(id)#danie obrazku na dol
        return id


    def Generate_Top_Left_Canvas_Background(self,verticles,normal, light_point, camera):
        z=-1.7976931348623157e+308
        self.m.top_Left_Background=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0],3),255,dtype=np.uint8)
        self.m.top_Left_Depth=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0]),z)
        #print 'normalne dla top left',normal
        for triangle_nr in range(0,len(self.m.triangle_Verticles)):
            triangle=self.m.triangle_Verticles[triangle_nr]
            points=(verticles[0:3,triangle[0]],verticles[0:3,triangle[1]],verticles[0:3,triangle[2]])
            #print 'TOP LEFT points',points
            #normal_Vector=self.Count_Normal_Vector(points)
            #normal_Vector=self.m.triangle_Normals[triangle_nr]
            normal_Vector=normal[triangle_nr]
            plane_Equation=self.Count_Plane(normal_Vector,points[0])

            for w in range(0,self.m.canvas_Resolution[0]):
                for h in range(0, self.m.canvas_Resolution[1]):
                    inside,cross_Point=self.Count_Cross_Point([w,h,0],np.array([w,h,1]),plane_Equation,points)
                    if inside:
                        #dist=self.count_3d_Distance(cross_Point,np.array([w,h,0]))
                        #print cross_Point[2]
                        #print self.m.top_Left_Depth[w,h]
            #zapamietac!!! > dla perspektywy widoku perspektywicznego a dla moich wydokow 3ch <
                        if self.m.top_Left_Depth[h,w]<cross_Point[2]:
                            self.m.top_Left_Depth[h,w]=cross_Point[2]
                            #print self.m.triangle_Color[triangle_nr]
                            color=self.phong_Color_Shading(triangle_nr,cross_Point,normal_Vector,light_point,camera)
                            #print self.m.triangle_Color[triangle_nr], triangle_nr
                            #self.m.top_Left_Background[h,w]=self.m.triangle_Color[triangle_nr]
                            self.m.top_Left_Background[h,w]=color



    def phong_Color_Shading(self,triangle_Nr,cross_Point,normal_Vector,light_point, camera):
       # print 'cross_Point',cross_Point
       # print 'light_point',light_point[:3]
        if np.dot(normal_Vector,light_point[:3]-cross_Point)<0:
            return self.m.triangle_Color[triangle_Nr]
        r=self.count_3d_Distance(cross_Point,camera)
        f=self.fatt(r)
        I=light_point[:3]-cross_Point
        dist=self.count_3d_Distance([0,0,0],I)
        if dist!=0:
            I=I/dist

        #Counting Os
        plane=self.Count_Plane(normal_Vector,cross_Point)#moana uzyc wczesniejszego
        point_under=self.find_point(camera[:3],camera[:3]+normal_Vector,plane)#mozna obliczyc raz na trojkat o ile nie ma cieniowania
        #print 'plane',plane

        vector0=cross_Point-point_under
        point_Os=camera[:3]+vector0+vector0
        Os=point_Os-cross_Point
        dist=self.count_3d_Distance([0,0,0],Os)
        if dist!=0:
            Os=Os/dist

        #test if angles between light and
       # print 'numer trojkata: ',triangle_Nr
        #Phong light model for each color(RGB)
        colors=[int(self.m.triangle_Color[triangle_Nr][i]+self.m.triangle_Surface[triangle_Nr][0]*f*self.m.light_Color[i]*np.dot(normal_Vector,I)+self.m.triangle_Surface[triangle_Nr][1]*f*self.m.light_Color[i]*pow(np.dot(I,Os),self.m.triangle_Surface[triangle_Nr][2])) for i in range(0,3)]


        for i in (0,1,2):
            if colors[i]>255:
                colors[i]=255
        return colors


    def find_point(self,start_point,second_point,plane_Equation):
        first_Line_Factor=np.array([start_point[0]-second_point[0],start_point[1]-second_point[1],start_point[2]-second_point[2]])
        top=-((second_point*plane_Equation[:3]).sum()+plane_Equation[3])
        bot=(plane_Equation[:3]*first_Line_Factor).sum()
        t=top/bot
        ret=first_Line_Factor*t+second_point
        return ret

    def fatt(self,r):
        #return min(1./(0.0005*pow(r,2)+r*0.001),1)
        return min(1./(r+1),1)

    def point_in_triangle(self,x,y, x0,y0, x1,y1, x2,y2):
    #barycentric algorithm
        x  -= x2 # przesuniecie wszystkich punktow
        x0 -= x2 # o wektor (-x2,-y2)
        x1 -= x2
        y  -= y2
        y0 -= y2
        y1 -= y2
        det = x0*y1 - y0*x1
        det = float(x0*y1 - y0*x1)
        if  abs(det) < 0.0000000000000000000000000000000001: # brak rozwiazan
            return False

        t0 = ( x*y1 -  y*x1)/det
        t1 = (x0*y  - y0*x )/det

        if t0 < 0 or t1 < 0 or t0+t1 > 1:
            return False
        else:
            return True

    def point_in_triangle1(self,x,y, x0,y0, x1,y1, x2,y2):
        #barycentric another one
        P=np.array([x,y])
        A=np.array([x0,y0])
        B=np.array([x1,y1])
        C=np.array([x2,y2])
        v0=C-A
        v1=B-A
        v2=P-A
        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        invDenom= 1./(dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom

        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v < 1)



    # punkty to trzyelementowe krotki (x,y,z)
    def point_in_triangle3D(self,p, p0,p1,p2):
        #print 'p0,p1,p2',p0,p1,p2
        x,y,z = p
        x0,y0,z0 = p0
        x1,y1,z1 = p1
        x2,y2,z2 = p2

        dx = max(x0,x1,x2) - min(x0,x1,x2) # wysokosci
        dy = max(y0,y1,y2) - min(y0,y1,y2) # prostopadloscianu
        dz = max(z0,z1,z2) - min(z0,z1,z2)

        min_height = min(dx,dy,dz)

        if dx == min_height: # plaszczyzna YZ: pomijamy wsp. x
            return self.point_in_triangle(y,z, y0,z0, y1,z1, y2,z2)

        if dy == min_height: # plaszczyzna ZX: pomijamy wsp. y
            return self.point_in_triangle(z,x, x0,z0, x1,z1, x2,z2)

        if dz == min_height: # plaszczyzna XY: pomijamy wsp. z
            return self.point_in_triangle(x,y, x0,y0, x1,y1, x2,y2)


    def Count_Cross_Point(self,start_point,second_point,plane_Equation,points):
        first_Line_Factor=np.array([start_point[0]-second_point[0],start_point[1]-second_point[1],start_point[2]-second_point[2]])

        top=-((second_point*plane_Equation[:3]).sum()+plane_Equation[3])
        bot=(plane_Equation[:3]*first_Line_Factor).sum()

        if (bot==0):
            return False, None
        t=top/bot
        ret=first_Line_Factor*t+second_point
        if self.point_in_triangle3D(ret,points[0],points[1],points[2]):
            return True, ret
        else:
            return False,None


    def Count_Normal_Vector(self,points):
        v0=points[0]-points[1]
        v1=points[2]-points[1]
        normal_Vector=np.cross(v1,v0)
        dist=self.count_3d_Distance([0,0,0],normal_Vector)
        return normal_Vector/dist

    def Count_Plane(self, normal_vector, point):
        D=-np.sum(point*normal_vector)
        return np.array([normal_vector[0],normal_vector[1],normal_vector[2],D])

    def count_3d_Distance(self,point1, point2):
        dist=math.sqrt(pow(long(point1[0])-long(point2[0]),2)+pow(long(point1[1])-long(point2[1]),2)+pow(long(point1[2])-long(point2[2]),2))
        return dist



    def Refresh_Top_Right_Canvas(self):
        to_Canvas_View=np.dot(self.translation(0,self.m.canvas_Resolution[1],0),self.scale_Matrix2(1,-1,1))
        verticles=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Verticles)
        light=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Light)
        camera=np.dot(to_Canvas_View,self.m.Top_Right_Canvas_Camera)
        normal= self.m.triangle_Normals.copy()
        normal[:,1]=-normal[:,1]
        background=self.Generate_Top_Right_Canvas_Background(verticles, normal, light, camera)
        #for i in self.m.triangle_Verticles:
         #   for j in range(-1,2):
                #i[j] indeks pierwszego wierzcholka i[j+1] indeks drugiego wierzcholka
          #      pass
          #      self.v.canvas_Top_Right.create_line(verticles[2][i[j]],verticles[1][i[j]],verticles[2][i[j+1]],verticles[1][i[j+1]])


        id=self.Set_Top_Right_Canvas()
        #danie obrazku na dol

    def Set_Top_Right_Canvas(self):
        image2 = Image.fromarray(self.m.top_Right_Background,'RGB')
        self.image_TK_TR = ImageTk.PhotoImage(image2)
        id=self.v.canvas_Top_Right.create_image(self.m.canvas_Resolution[0]/2, self.m.canvas_Resolution[1]/2, image=self.image_TK_TR)
        self.v.canvas_Top_Right.lower(id)
        return id

    def Generate_Top_Right_Canvas_Background(self, verticles, normal, light_point, camera):
        z=1.7976931348623157e+308
        self.m.top_Right_Background=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0],3),255,dtype=np.uint8)
        self.m.top_Right_Depth=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0]),z)

        for triangle_nr in range(0,len(self.m.triangle_Verticles)):
            triangle=self.m.triangle_Verticles[triangle_nr]
            points=(verticles[0:3,triangle[0]],verticles[0:3,triangle[1]],verticles[0:3,triangle[2]])
            #print 'TOP RIGHTpoints',points

            #punkty wygladaja dobrze
            normal_Vector=normal[triangle_nr]
            plane_Equation=self.Count_Plane(normal_Vector,points[0])
            #print self.m.canvas_Resolution
           # print 'test'
            #print 'triangle_nr',triangle_nr
            #inside,cross_Point=self.Count_Cross_Point([0,40,364],np.array([1,40,364]),plane_Equation,points)
            #print 'inside,cross_Point',inside,cross_Point

            for w in range(0,self.m.canvas_Resolution[0]):
                for h in range(0, self.m.canvas_Resolution[1]):
                    #print 'w,h', w,h

                    #to za chwile odznaczyc
                    inside,cross_Point=self.Count_Cross_Point([0,h,w],np.array([1,h,w]),plane_Equation,points)
                    #np.array([-26.63495317,40,364])


                    #print 'inside,cross_Point',inside,cross_Point
                    if inside:
                        #dist=self.count_3d_Distance(cross_Point,np.array([w,h,0]))
                        #print cross_Point[2]
                        #print self.m.top_Left_Depth[w,h]
            #zapamietac!!! > dla perspektywy widoku perspektywicznego a
                        if self.m.top_Right_Depth[h,w]>cross_Point[0]:
                            self.m.top_Right_Depth[h,w]=cross_Point[0]
                            color=self.phong_Color_Shading(triangle_nr,cross_Point,normal_Vector,light_point,camera)
                            #print self.m.triangle_Color[triangle_nr], triangle_nr
                           # print 'self.m.triangle_Color[triangle_nr]',self.m.triangle_Color[triangle_nr]

                            #self.m.top_Right_Background[h,w]=self.m.triangle_Color[triangle_nr]
                            self.m.top_Right_Background[h,w]=color

            #self.m.top_Right_Background[40,364]=[0,255,0]
        #print self.m.top_Right_Background




    def Refresh_Bottom_Left_Canvas(self):

        #tworzymy reprezentacje punktow w macierzy NUMPY i wrzucamy to jako obraz do CANVASU
        to_Canvas_View=np.dot(self.translation(0,0,self.m.canvas_Resolution[1]),self.scale_Matrix2(1,1,-1))
        verticles=np.dot(to_Canvas_View,self.m.Bottom_Left_Canvas_Verticles)
        light=np.dot(to_Canvas_View,self.m.Bottom_Left_Canvas_Light)
        camera=np.dot(to_Canvas_View,self.m.Bottom_Left_Canvas_Camera)
        #print 'camera: ',camera
        normal= self.m.triangle_Normals.copy()
        normal[:,2]=-normal[:,2]
        ##chwilowe rozwiazanie by sprawdzic jak wyglada to wszystko po przeksztalceniach
        #print  len(self.m.triangle_Verticles)
        background=self.Generate_Bottom_Left_Canvas_Background(verticles, normal, light, camera)
        id=self.Set_Bottom_Left_Canvas()
        #self.v.canvas_Bottom_Left.lower(id)#danie obrazku na dol
        for i in self.m.triangle_Verticles:
            for j in range(-1,2):
                #i[j] indeks pierwszego wierzcholka i[j+1] indeks drugiego wierzcholka
              #  pass
                self.v.canvas_Bottom_Left.create_line(verticles[0][i[j]],verticles[2][i[j]],verticles[0][i[j+1]],verticles[2][i[j+1]])



    def Set_Bottom_Left_Canvas(self):
        image2 = Image.fromarray(self.m.bottom_Left_Background,'RGB')
        #image2.show()
        self.image_TK_BL = ImageTk.PhotoImage(image2)
        id=self.v.canvas_Bottom_Left.create_image(self.m.canvas_Resolution[0]/2, self.m.canvas_Resolution[1]/2, image=self.image_TK_BL)
        self.v.canvas_Bottom_Left.lower(id)
        return id


    def Generate_Bottom_Left_Canvas_Background(self, verticles, normal, light_point, camera):
        z=1.7976931348623157e+308
        self.m.BLP=True
        self.m.bottom_Left_Background=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0],3),255,dtype=np.uint8)
        self.m.bottom_Left_Depth=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0]),z)

        for triangle_nr in range(0,len(self.m.triangle_Verticles)):
            self.m.numer=triangle_nr
            triangle=self.m.triangle_Verticles[triangle_nr]
            points=(verticles[0:3,triangle[0]].copy(),verticles[0:3,triangle[1]].copy(),verticles[0:3,triangle[2]].copy())
            normal_Vector=normal[triangle_nr]
            #print 'BOTTOM LEFT points',points

            plane_Equation=self.Count_Plane(normal_Vector,points[0])
            #print 'plane_Equation',plane_Equation
            #print 'plane_Equation',plane_Equation
            for w in range(0,self.m.canvas_Resolution[0]):
                for h in range(0, self.m.canvas_Resolution[1]):
                    inside,cross_Point=self.Count_Cross_Point([w,0,h],np.array([w,-1,h]),plane_Equation,points)
                    #if(inside and (cross_Point[1]!=w or cross_Point[2]!=h)):
                     #   print 'cos z punktami sie jeblo: w,h:', w,h
                    if inside:
            #zapamietac!!! > dla perspektywy widoku perspektywicznego a
                        if self.m.bottom_Left_Depth[h,w]>cross_Point[1]:
                            self.m.bottom_Left_Depth[h,w]=cross_Point[1]
                            #color=self.phong_Color_Shading(triangle_nr,cross_Point,normal_Vector,light_point,camera)
                            #print self.m.triangle_Color[triangle_nr], triangle_nr
                           # print 'self.m.triangle_Color[triangle_nr]',self.m.triangle_Color[triangle_nr]

                            self.m.bottom_Left_Background[h,w]=self.m.triangle_Color[triangle_nr]

                            #self.m.Bottom_Left_Background[h,w]=color

            #self.m.top_Right_Background[40,364]=[0,255,0]
        #print self.m.top_Right_Background


    def Refresh_Bottom_Right_Canvas(self):

      #  to_Canvas_View=np.dot(self.translation(0,0,self.m.canvas_Resolution[1]),self.scale_Matrix2(1,1,-1))
        verticles=self.m.verticles
        light=self.m.light_Position
        camera=self.m.camera_Position
        #print 'camera: ',camera
        normal= self.m.triangle_Normals.copy()

        background=self.Generate_Bottom_Right_Canvas_Background(verticles, normal, light, camera)
        id=self.Set_Bottom_Right_Canvas()
        #self.v.canvas_Bottom_Left.lower(id)#danie obrazku na dol

    def find_pixel_Coord(self,w,h):
        #uaywasz rezolucji
        viewpoint_Rectangle=self.m.camera_Rectangle_Points.copy()
        b=viewpoint_Rectangle[0]-viewpoint_Rectangle[3]
        a=viewpoint_Rectangle[2]-viewpoint_Rectangle[3]
        B=b/(self.m.canvas_Resolution[0]-1)
        A=a/(self.m.canvas_Resolution[1]-1)
        dx=w*B
        dy=h*A
        pixel_Coords=viewpoint_Rectangle[3]+dx+dy
        return pixel_Coords

    def Generate_Bottom_Right_Canvas_Background(self, verticles, normal, light_point, camera):
        z=1.7976931348623157e+308
        self.m.bottom_Right_Background=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0],3),255,dtype=np.uint8)
        self.m.bottom_Right_Depth=np.full((self.m.canvas_Resolution[1],self.m.canvas_Resolution[0]),z)

        for triangle_nr in range(0,len(self.m.triangle_Verticles)):
            triangle=self.m.triangle_Verticles[triangle_nr]
            points=(verticles[triangle[0],0:3],verticles[triangle[1],0:3],verticles[triangle[2],0:3])
            #print 'TOP RIGHTpoints',points

            #punkty wygladaja dobrze
            normal_Vector=normal[triangle_nr]
            plane_Equation=self.Count_Plane(normal_Vector,points[0])
           # print self.m.canvas_Resolution
           # print 'test'
            #print 'triangle_nr',triangle_nr
            #inside,cross_Point=self.Count_Cross_Point([0,40,364],np.array([1,40,364]),plane_Equation,points)
            #print 'inside,cross_Point',inside,cross_Point

            for w in range(0,self.m.canvas_Resolution[0]):
                for h in range(0, self.m.canvas_Resolution[1]):
                    #print 'w,h', w,h


                    viewpoint_Pixel= self.find_pixel_Coord(w,h)
                    inside,cross_Point=self.Count_Cross_Point(viewpoint_Pixel[:3],camera[:3],plane_Equation,points)
                    #np.array([-26.63495317,40,364])

                    #a=self.m.viewport_Position[0:3]-self.m.camera_Position[0:3]
                    #b=cross_Point[0:3]-self.m.viewport_Position[0:3]

                    if inside :
                        temp=np.dot(self.m.viewport_Position[0:3]-self.m.camera_Position[0:3],cross_Point[0:3]-self.m.viewport_Position[0:3])
                        if np.dot(self.m.viewport_Position[0:3]-self.m.camera_Position[0:3],cross_Point[0:3]-self.m.viewport_Position[0:3])>=0:

                        #print 'inside,cross_Point',inside,cross_Point

                            dist=self.count_3d_Distance(cross_Point,camera)
                            if self.m.bottom_Right_Depth[h,w]>dist:
                                self.m.bottom_Right_Depth[h,w]=dist
                                #color=self.phong_Color_Shading(triangle_nr,cross_Point,normal_Vector,light_point,camera)
                                #print self.m.triangle_Color[triangle_nr], triangle_nr
                               # print 'self.m.triangle_Color[triangle_nr]',self.m.triangle_Color[triangle_nr]

                                self.m.bottom_Right_Background[h,w]=self.m.triangle_Color[triangle_nr]
                                #self.m.bottom_Right_Background[h,w]=color

            #self.m.top_Right_Background[40,364]=[0,255,0]
        #print self.m.top_Right_Background


    def Set_Bottom_Right_Canvas(self):
        image2 = Image.fromarray(self.m.bottom_Right_Background,'RGB')
        #image2=ImageOps.flip(image2)
        #image2.show()
        self.image_TK_BR = ImageTk.PhotoImage(image2)
        id=self.v.canvas_Bottom_Right.create_image(self.m.canvas_Resolution[0]/2, self.m.canvas_Resolution[1]/2, image=self.image_TK_BR)
        return id




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

    def Draw_Top_Left_Camera_Triangle1(self, matrix):
        camera=np.dot(matrix,self.m.Top_Left_Canvas_Camera)
        viewport=np.dot(matrix,self.m.Top_Left_Canvas_Viewpoint)
        points=np.dot(matrix,self.m.Top_Left_Canvas_Rectangle)
        lines_before_cut=[]

        self.m.clickable_Points['Top_Left_Camera']=camera
        self.m.clickable_Points['Top_Left_Viewpoint']=viewport

        self.v.canvas_Top_Left.create_line(camera[0],camera[1], viewport[0], viewport[1],fill='red', width=3 )

        for i in range(0,4):
            lines_before_cut.append((camera[0],camera[1],points[0][i],points[1][i]))
        for i in range(-1,3):
            lines_before_cut.append((points[0][i],points[1][i],points[0][i+1],points[1][i+1]))
        lines_after_cut=self.cut_Lines( self.m.canvas_Resolution[0], self.m.canvas_Resolution[1], lines_before_cut)
        for i in range(-1,len(lines_after_cut)):
            self.v.canvas_Top_Left.create_line(lines_after_cut[i][0],lines_after_cut[i][1],lines_after_cut[i][2],lines_after_cut[i][3])



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
            self.v.canvas_Top_Right.create_line(points[2][i]
                                                ,points[1][i],points[2][i+1],points[1][i+1])


    #biblioteka obcinajaca przyjmujaca (x,y-max i min 0,0) i obcinajaca cos powyzej
    def cut_Lines(self,x_max,y_max,lines):
        #wyznacz wektor
        #Cohen,Sutherland vector
        first_Point_Vector=[]
        second_point_Vector=[]
        cutted_lines=[]
        #for i in lines:
            # i mam (xo,yo,x1,y1)
            #(top,bot,left,right)
            #punkt o
         #   first_Point_Vector.append((y<i[1],i[1]<0,i[0]<0,i[0]>x))
          #  second_point_Vector.append((y<i[3],i[3]<0,i[2]<0,i[2]>x))
        #print 'co ja tutaj kurwa robie'
        #print first_Point_Vector
        #print'sec'
        #print second_point_Vector
        #print lines
        for i in lines:
            i=list(i)
            B1=(y_max<i[1],i[1]<0,i[0]<0,i[0]>x_max)
            B2=(y_max<i[3],i[3]<0,i[2]<0,i[2]>x_max)
            while(True):
                if(B1==(0,0,0,0) and B2==(0,0,0,0)):
                    cutted_lines.append(tuple(i))
                    break
                elif((B1 and B2)!=(0,0,0,0) ):
                    break
                else:
                    #Cutting
                    #wybieramy punkt w srodku
                    ktory=-1
                    x=0
                    y=0

                    if(B1!=(0,0,0,0)):
                        b=B1
                        ktory=1
                    else:
                        b=B2
                        ktory=2

                    if b[0]:
                        #ciecie gorna krawedzia
                        x=i[0]+(i[2]-i[0])*(y_max-i[1])/(i[3]-i[1])
                        y=y_max
                    elif b[1]:
                        #ciecie dolna krawdzia okna
                        x=i[0]+(i[2]-i[0])*(0-i[1])/(i[3]-i[1])
                        y=y_max
                    elif b[2]:
                        y=i[1]+(i[3]-i[1])*(0-i[0])/(i[2]-i[0])
                        x=0
                    else:
                        y=i[1]+(i[3]-i[1])*(x_max-i[0])/(i[2]-i[0])
                        x=x_max

                    if(ktory==1):
                        i[0],i[1]=x,y
                        B1=(y_max<i[1],i[1]<0,i[0]<0,i[0]>x_max)
                    else:
                        i[2],i[3]=x,y
                        B2=(y_max<i[3],i[3]<0,i[2]<0,i[2]>x_max)

        return cutted_lines


    def click_Top_Left(self,x,y):
        #sprawdzenie ktory piunkt na canvasie to left
        #test dla Camery
        #print self.m.clickable_Points["Top_Left_Viewpoint"]
        #print self.m.clickable_Points["Top_Left_Camera"]

        #sprawdzenie czy ejst obiekt
        if(self.m.have_Object):
            viewpoint= self.m.clickable_Points["Top_Left_Viewpoint"]
            camera=self.m.clickable_Points["Top_Left_Camera"]
            #sprawdzamy czy jest w otoczeniu +-5 w x i y camery
            if -5<x-camera[0]<5 and -5<y-camera[1]<5:
                self.clicked_Type="Camera"
                self.clicked_Top_Left_Camera(x,y)
            elif -5<x-viewpoint[0]<5 and -5<y-viewpoint[1]<5:
                self.clicked_Type="Viewport"
                self.clicked_Top_Left_Viewport(x,y)

    def clicked_Top_Left_Camera(self,x,y):
        self.m.clicked_Point_Position[0],self.m.clicked_Point_Position[1]=x,y
        self.m.backup_camera=self.m.camera_Position.copy()

    def clicked_Top_Left_Viewport(self,x,y):
        self.m.clicked_Point_Position[0],self.m.clicked_Point_Position[1]=x,y
        self.m.backup_viewport=self.m.viewport_Position.copy()

    def motion_Top_Left(self,x,y):
        if(self.m.have_Object):
            if self.clicked_Type=="Camera":
                self.motion_Top_Left_Camera(x,y)
            elif self.clicked_Type=="Viewport":
                self.motion_Top_Left_Viewport(x,y)


    def motion_Top_Left_Viewport(self,x,y):
        dif_X,dif_Y=x-self.m.clicked_Point_Position[0],-(y-self.m.clicked_Point_Position[1])
        mult=self.m.prescaler*self.m.zoom_Canvas[0]/10.
        dif_X=dif_X/mult
        dif_Y=dif_Y/mult
        self.m.viewport_Position[0]=self.m.backup_viewport[0]+dif_X
        self.m.viewport_Position[1]=self.m.backup_viewport[1]+dif_Y
        self.set_Camera_Rectangle_Points()
        self.clear_Canvas()
        self.set_Canvas()


    def motion_Top_Left_Camera(self,x,y):
        dif_X,dif_Y=x-self.m.clicked_Point_Position[0],-(y-self.m.clicked_Point_Position[1])
        mult=self.m.prescaler*self.m.zoom_Canvas[0]/10.
        dif_X=dif_X/mult
        dif_Y=dif_Y/mult
        self.m.camera_Position[0]=self.m.backup_camera[0]+dif_X
        self.m.camera_Position[1]=self.m.backup_camera[1]+dif_Y
        self.set_Camera_Rectangle_Points()
        self.clear_Canvas()
        self.set_Canvas()

    def release_Top_Left(self):
        self.m.Refresh_Camera_View=True
        self.clicked_Type=''



    #tutaj zaczynam modyfokacje top right
    def click_Top_Right(self,x,y):
        #print self.m.clickable_Points["Top_Right_Viewpoint"]
        #print self.m.clickable_Points["Top_Right_Camera"]

        #sprawdzenie czy ejst obiekt
        if(self.m.have_Object):
            viewpoint= self.m.clickable_Points["Top_Right_Viewpoint"]
            camera=self.m.clickable_Points["Top_Right_Camera"]
            #sprawdzamy czy jest w otoczeniu +-5 w x i y camery
            if -5<x-camera[2]<5 and -5<y-camera[1]<5:
                self.clicked_Type="Camera"
                self.clicked_Top_Right_Camera(x,y)
            elif -5<x-viewpoint[2]<5 and -5<y-viewpoint[1]<5:
                self.clicked_Type="Viewport"
                self.clicked_Top_Right_Viewport(x,y)

    def clicked_Top_Right_Camera(self,x,y):
        #x is Z axis
        self.m.clicked_Point_Position[0],self.m.clicked_Point_Position[1]=x,y
        self.m.backup_camera=self.m.camera_Position.copy()

    def clicked_Top_Right_Viewport(self,x,y):
        self.m.clicked_Point_Position[0],self.m.clicked_Point_Position[1]=x,y
        self.m.backup_viewport=self.m.viewport_Position.copy()

    def motion_Top_Right(self,x,y):
        if(self.m.have_Object):
            if self.clicked_Type=="Camera":
                self.motion_Top_Right_Camera(x,y)
            elif self.clicked_Type=="Viewport":
                self.motion_Top_Right_Viewport(x,y)


    def motion_Top_Right_Viewport(self,x,y):
        dif_X,dif_Y=x-self.m.clicked_Point_Position[0],-(y-self.m.clicked_Point_Position[1])
        mult=self.m.prescaler*self.m.zoom_Canvas[1]/10.
        dif_X=dif_X/mult
        dif_Y=dif_Y/mult
        self.m.viewport_Position[2]=self.m.backup_viewport[2]+dif_X
        self.m.viewport_Position[1]=self.m.backup_viewport[1]+dif_Y
        self.set_Camera_Rectangle_Points()
        self.clear_Canvas()
        self.set_Canvas()


    def motion_Top_Right_Camera(self,x,y):
        dif_X,dif_Y=x-self.m.clicked_Point_Position[0],-(y-self.m.clicked_Point_Position[1])
        mult=self.m.prescaler*self.m.zoom_Canvas[1]/10.
        dif_X=dif_X/mult
        dif_Y=dif_Y/mult
        self.m.camera_Position[2]=self.m.backup_camera[2]+dif_X
        self.m.camera_Position[1]=self.m.backup_camera[1]+dif_Y
        self.set_Camera_Rectangle_Points()
        self.clear_Canvas()
        self.set_Canvas()

    def release_Top_Right(self):
        self.m.Refresh_Camera_View=True
        self.clicked_Type=''

    #a tutaj koncze modyfikacja top right

    def click_Bottom_Left(self,x,y):
        #sprawdzenie ktory piunkt na canvasie to left
        #test dla Camery
        #print self.m.clickable_Points["Bottom_Left_Viewpoint"]
        #print self.m.clickable_Points["Bottom_Left_Camera"]

        #sprawdzenie czy ejst obiekt
        if(self.m.have_Object):
            viewpoint= self.m.clickable_Points["Bottom_Left_Viewpoint"]
            camera=self.m.clickable_Points["Bottom_Left_Camera"]
            #sprawdzamy czy jest w otoczeniu +-5 w x i y camery
            if -5<x-camera[0]<5 and -5<y-camera[2]<5:
                self.clicked_Type="Camera"
                self.clicked_Bottom_Left_Camera(x,y)
            elif -5<x-viewpoint[0]<5 and -5<y-viewpoint[2]<5:
                self.clicked_Type="Viewport"
                self.clicked_Bottom_Left_Viewport(x,y)

    def clicked_Bottom_Left_Camera(self,x,y):
        self.m.clicked_Point_Position[0],self.m.clicked_Point_Position[1]=x,y
        self.m.backup_camera=self.m.camera_Position.copy()

    def clicked_Bottom_Left_Viewport(self,x,y):
        self.m.clicked_Point_Position[0],self.m.clicked_Point_Position[1]=x,y
        self.m.backup_viewport=self.m.viewport_Position.copy()

    def motion_Bottom_Left(self,x,y):
        if(self.m.have_Object):
            if self.clicked_Type=="Camera":
                self.motion_Bottom_Left_Camera(x,y)
            elif self.clicked_Type=="Viewport":
                self.motion_Bottom_Left_Viewport(x,y)


    def motion_Bottom_Left_Viewport(self,x,y):
        dif_X,dif_Y=x-self.m.clicked_Point_Position[0],-(y-self.m.clicked_Point_Position[1])
        mult=self.m.prescaler*self.m.zoom_Canvas[2]/10.
        dif_X=dif_X/mult
        dif_Y=dif_Y/mult
        self.m.viewport_Position[0]=self.m.backup_viewport[0]+dif_X
        self.m.viewport_Position[2]=self.m.backup_viewport[2]+dif_Y
        self.set_Camera_Rectangle_Points()
        self.clear_Canvas()
        self.set_Canvas()


    def motion_Bottom_Left_Camera(self,x,y):
        dif_X,dif_Y=x-self.m.clicked_Point_Position[0],-(y-self.m.clicked_Point_Position[1])
        mult=self.m.prescaler*self.m.zoom_Canvas[2]/10.
        dif_X=dif_X/mult
        dif_Y=dif_Y/mult
        self.m.camera_Position[0]=self.m.backup_camera[0]+dif_X
        self.m.camera_Position[2]=self.m.backup_camera[2]+dif_Y
        self.set_Camera_Rectangle_Points()
        self.clear_Canvas()
        self.set_Canvas()

    def release_Bottom_Left(self):
        self.m.Refresh_Camera_View=True
        self.clicked_Type=''


    def clear_Canvas(self):
        self.v.canvas_Top_Right.delete('all')
        self.v.canvas_Top_Left.delete('all')
        self.v.canvas_Bottom_Left.delete('all')
        self.v.canvas_Bottom_Right.delete('all')


if __name__=='__main__':
    c=Controller()
    c.v.Start_App()


