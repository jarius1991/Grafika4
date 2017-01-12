import ttk
from Tkinter import *
import Controller

#komentarze zrobic

#jak zobie poradzic z canvasem/OpenGL?

class View():
    def __init__(self,control):
        self.control=control#klasa kontrolera przyjmujaca polecenia z metod w srodku
        self.Init_App_Window()
        self.Init_Buttons()
        self.Init_Camera_Angle_Scale()
        self.Init_Canvas()
        self.Init_Canvas_Buttons()



    def Start_App(self):
        self.root.mainloop()

    def Init_App_Window(self):
        self.root=Tk()
        self.frame=ttk.Frame(self.root)
        self.root.title("CG - TASK4")
        self.frame.grid(column=0,row=0,sticky=(N,S,E,W))
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        self.root.minsize(width=1000,height=1000)
       # self.root.bind("<Configure>", self.On_Resize)

        for i in (0,1):
            self.frame.grid_columnconfigure(i,weight=1)
            self.frame.grid_rowconfigure(i,weight=1)

    def On_Resize(self, *args):
       # self.control.Resize_Window()
        pass
        print "Zmiana romiaru"


    def Init_Buttons(self):
        self.open_Button=ttk.Button(self.frame,text='Open' ,command=self.Open_Model,padding=[10,10,10,10])
        self.save_Button=ttk.Button(self.frame,text='Save' ,command=self.Save_Model,padding=[10,10,10,10])
        self.open_Button.grid(column=1, row=2,sticky=(E), padx=10, pady=10)
        self.save_Button.grid(column=1, row=3,sticky=(E), padx=10, pady=10)
        #self.frame.grid_rowconfigure(2, weight=1)
        #self.frame.grid_columnconfigure(1, weight=1)

    def Init_Camera_Angle_Scale(self):
        self.angle_Camera=IntVar()
        self.label=ttk.Label(self.frame,text="Angle of camera")#,padding=[10,10,10,10])
        self.scale_Item=ttk.Scale(self.frame, orient=HORIZONTAL, length=400, from_=1.0, to=89.0, variable=self.angle_Camera, command=self.Scale_Change)
        self.label.grid(column=0 ,row=2, padx=10, pady=10,sticky=(W))
        self.scale_Item.grid(column=0, row=3, padx=10, pady=10,sticky=(W))
        self.scale_Item.bind("<ButtonRelease-1>", self.Update_Scale_Value)
        #self.angle_Camera.set(45)

    def Init_Canvas(self):
        self.canvas_Top_Left=Canvas(self.frame,  background='#ffffff')
        self.canvas_Top_Right=Canvas(self.frame,  background='#ffffff')
        self.canvas_Bottom_Left=Canvas(self.frame,  background='#ffffff')
        self.canvas_Bottom_Right=Canvas(self.frame,  background='#ffffff')

        self.canvas_Top_Left.grid(column=0, row=0, sticky=(N,S,E,W))
        self.canvas_Top_Right.grid(column=1, row=0, sticky=(N,S,E,W))
        self.canvas_Bottom_Left.grid(column=0, row=1, sticky=(N,S,E,W))
        self.canvas_Bottom_Right.grid(column=1, row=1, sticky=(N,S,E,W))

        for i in (0,1):
            self.frame.grid_rowconfigure(i,weight=1)
            self.frame.grid_columnconfigure(i,weight=1)

        self.canvas_Top_Left.bind("<Button-1>",self.click_Top_Left)
        self.canvas_Top_Left.bind("<B1-Motion>",self.motion_Top_Left)
        self.canvas_Top_Left.bind("<ButtonRelease-1>",self.release_Top_Left)

        self.canvas_Top_Right.bind("<Button-1>",self.click_Top_Right)
        self.canvas_Top_Right.bind("<B1-Motion>",self.motion_Top_Right)
        self.canvas_Top_Right.bind("<ButtonRelease-1>",self.release_Top_Right)

        self.canvas_Bottom_Left.bind("<Button-1>",self.click_Bottom_Left)
        self.canvas_Bottom_Left.bind("<B1-Motion>",self.motion_Bottom_Left)
        self.canvas_Bottom_Left.bind("<ButtonRelease-1>",self.release_Bottom_Left)


    def click_Top_Left(self,event):
        self.control.click_Top_Left(event.x,event.y)

    def motion_Top_Left(self,event):
        self.control.motion_Top_Left(event.x,event.y)

    def release_Top_Left(self,event):
        self.control.release_Top_Left()


    def click_Bottom_Left(self,event):
        self.control.click_Bottom_Left(event.x,event.y)

    def motion_Bottom_Left(self,event):
        self.control.motion_Bottom_Left(event.x,event.y)

    def release_Bottom_Left(self,event):
        self.control.release_Bottom_Left()


    def click_Top_Right(self,event):
        self.control.click_Top_Right(event.x,event.y)

    def motion_Top_Right(self,event):
        self.control.motion_Top_Right(event.x,event.y)

    def release_Top_Right(self,event):
        self.control.release_Top_Right()


    def Init_Canvas_Buttons(self):
        self.plus_Top_Left_Button=ttk.Button(self.frame, text='+',padding=[10,10,10,10], command=self.Plus_Top_Left_Button_Clicked, state=DISABLED)
        self.plus_Top_Right_Button=ttk.Button(self.frame, text='+',padding=[10,10,10,10], command=self.Plus_Top_Right_Button_Clicked, state=DISABLED)
        self.plus_Bottom_Left_Button=ttk.Button(self.frame, text='+',padding=[10,10,10,10], command=self.Plus_Bottom_Left_Button_Clicked, state=DISABLED)
      #  self.plus_Bottom_Right_Button=ttk.Button(self.frame, text='+',padding=[10,10,10,10], command=self.Plus_Bottom_Right_Button_Clicked, state=DISABLED)

        self.minus_Top_Left_Button=ttk.Button(self.frame, text='-',padding=[10,10,10,10], command=self.Minus_Top_Left_Button_Clicked)
        self.minus_Top_Right_Button=ttk.Button(self.frame, text='-',padding=[10,10,10,10], command=self.Minus_Top_Right_Button_Clicked)
        self.minus_Bottom_Left_Button=ttk.Button(self.frame, text='-',padding=[10,10,10,10], command=self.Minus_Bottom_Left_Button_Clicked)
      #   self.minus_Bottom_Right_Button=ttk.Button(self.frame, text='-',padding=[10,10,10,10], command=self.Minus_Bottom_Right_Button_Clicked)

        self.plus_Top_Left_Button.grid(column=0, row=0, sticky=(N,W))
        self.plus_Top_Right_Button.grid(column=1, row=0, sticky=(N,W))
        self.plus_Bottom_Left_Button.grid(column=0, row=1, sticky=(N,W))
      #   self.plus_Bottom_Right_Button.grid(column=1, row=1, sticky=(N,W))

        self.minus_Top_Left_Button.grid(column=0, row=0, sticky=(N,E))
        self.minus_Top_Right_Button.grid(column=1, row=0, sticky=(N,E))
        self.minus_Bottom_Left_Button.grid(column=0, row=1, sticky=(N,E))
      #   self.minus_Bottom_Right_Button.grid(column=1, row=1, sticky=(N,E))


    def Plus_Top_Left_Button_Clicked(self):
        self.control.Zoom_Top_Left_Plus()

    def Plus_Top_Right_Button_Clicked(self):
        self.control.Zoom_Top_Right_Plus()

    def Plus_Bottom_Left_Button_Clicked(self):
        self.control.Zoom_Bottom_Left_Plus()

    def Minus_Top_Left_Button_Clicked(self):
        self.control.Zoom_Top_Left_Minus()
        #self.minus_Top_Left_Button['state']=DISABLED

    def Minus_Top_Right_Button_Clicked(self):
        self.control.Zoom_Top_Right_Minus()

    def Minus_Bottom_Left_Button_Clicked(self):
        self.control.Zoom_Bottom_Left_Minus()







    def Open_Model(self):
        self.control.Open_Data()

    def Save_Model(self):
       # print self.canvas_Top_Left.winfo_width(),self.canvas_Top_Left.winfo_height()
        self.control.Save_Camera()
       # pass#powinien przekazywac akcje do kontrolera
        #print self.canvas_Top_Left.cget('cursor')

    def Scale_Change(self,*args):
       # print self.angle_Camera.get()
        self.control.angle_Change(self.angle_Camera.get())

    def Update_Scale_Value(self,*args):
       self.control.angle_Update()





