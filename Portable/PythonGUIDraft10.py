import tkinter as tk
import numpy as np
import xbox
import time
from adafruit_motorkit import MotorKit
kit = MotorKit()

'''
Motor 1 = Y
Motor 2 = X
Motor 3 = -Y
Motor 4 = -X
'''


window = tk.Tk() #initilize a window
window.title("MagneticFieldGui")
#icon = tk.PhotoImage(file = "/home/bizzaro/Desktop/MagneticApp/GUI/MMM.png")
#window.iconphoto(True, icon)

# get the screen dimension

window.geometry("800x480")
window.attributes('-fullscreen', True)

rows = [0,1,2,3,4,5,6,7]
columns = [0,1,2,3,4,5,6,7]
window.columnconfigure(rows, minsize=100)
window.rowconfigure(columns, minsize = 60)

'''
for i in range(len(rows)):
    for j in range(len(columns)):
        frame = tk.Frame(master = window,
                          width = 100,
                          height = 60,
                          relief = tk.RAISED,
                          borderwidth = 5)
        frame.grid(row = rows[i], column = columns[j])
'''

#Initilize textbox to update with tousputs from each button
Text_Box = tk.Text(master = window, width = 22, height = 12)
Scroll_Bar = tk.Scrollbar(master= window, command = Text_Box.yview, orient = 'vertical')
Text_Box.configure(yscrollcommand = Scroll_Bar.set)
Text_Box.grid(row = 3, column = 6, rowspan = 4, columnspan = 2, sticky = "nwse")






Duty_Cycle = 0 #MAY NEED TO CHANGE ; MAY CAUSE NOISE
# Create Slider to Vary the Strength
def Set_Speed(Scale_Value1):
    global Duty_Cycle
    Duty_Cycle = Scale_Value1
    Field_Strength_Entry.delete(0, tk.END)
    Field_Strength_Entry.insert(0, str(Duty_Cycle))
     
  
    
Scale_Value1 = tk.DoubleVar()
Horizontal_Slider = tk.Scale(master = window, from_ = 0, to=1, variable = Scale_Value1,
                             orient = tk.HORIZONTAL, resolution = 0.01, command = Set_Speed, 
                             width = 50, length = 300, showvalue = 0)
Horizontal_Slider.grid(row = 0, column = 2, columnspan =3, rowspan = 1)


#Create Gauge and initlize Pointer
Gauge = tk.Canvas(master = window)
Circle_Coords = 0,0,360,360  # 60 pixels x 6 rows
Circ = Gauge.create_oval(Circle_Coords,fill = 'white' ,width = 1)
YAxis = Gauge.create_line(180, 0,180,360, width = 1, fill = "black")
Xaxis = Gauge.create_line(0,180,360,180, width = 1, fill = "black")
Pointer = Gauge.create_line(0,0,0,0)
Gauge.grid(row = 2, column = 2, columnspan = 4, rowspan = 6,sticky = "wnse")

#Update Arrow Function
def Move_Arrow(Direction):
    global Pointer
    R = 180 #Radius of cicle
    X_Comp = R+R*np.cos(Direction * np.pi/180)
    Y_Comp = R-R*np.sin(Direction * np.pi/180) 
    Start_Point = R, R 
    End_Point = X_Comp, Y_Comp
    
    Gauge.delete(Pointer)
    Pointer = Gauge.create_line(Start_Point, End_Point, arrow = tk.LAST, width = 4, fill = "black", arrowshape = (15,20,8))
    Gauge.grid(row = 2, column = 2, columnspan = 4, rowspan = 6, sticky = "nswe")
    




# Create Slider to Vary the Direction
def Set_Direction(Scale_Value2):
    global Direction_Val
    Direction_Val = Scale_Value2
    Field_Direction_Entry.delete(0, tk.END)
    Field_Direction_Entry.insert(0, str(Direction_Val))
   
    Move_Arrow(int(Field_Direction_Entry.get()))
    
    
Scale_Value2 = tk.DoubleVar()
Horizontal_Slider = tk.Scale(master = window, from_ = 0, to=360, variable = Scale_Value2,
                             orient = tk.HORIZONTAL, resolution = 5, command = Set_Direction, 
                             width = 50, length = 300, showvalue = 0)
Horizontal_Slider.grid(row = 1, column = 2, columnspan =3, rowspan = 1) 






start_time_list = []
end_time_list = []
Data_Vector_List = []  #Strores the field angle, magnitude, and elpased time from when the apply button is pressed to when the zero button is pressed
#Field Strength and Direction
def Handle_Apply():   
    '''
    need to add the code that will turn on each coil that represents the proper duty cycle.
    '''
    global Field_Angle 
    global Field_Mag

    Field_Angle = float(Field_Direction_Entry.get())
    Field_Mag = float(Field_Strength_Entry.get())
    #Field_Strength_Entry.insert(0, Field_Mag)
    
    X_Duty_Cycle = round(Field_Mag * np.cos(Field_Angle * np.pi/180),2)
    Y_Duty_Cycle = round(Field_Mag * np.sin(Field_Angle * np.pi/180),2)
    print(X_Duty_Cycle, Y_Duty_Cycle)
    #print(Duty_Cycle)
    kit.motor1.throttle = Y_Duty_Cycle  #converging
    kit.motor2.throttle = X_Duty_Cycle  #converging
    kit.motor3.throttle = -Y_Duty_Cycle #diverging
    kit.motor4.throttle = -X_Duty_Cycle #diverging
    
    #Begin Data Capture
    start = time.time()
    start_time_list.append(start)
    
   
    
    
    
    
def Handle_Zero():
    
    '''
    need to add the code that will turn off all signals to ALL electromagnetic coils
    '''
    #Field_Strength_Entry.delete(0, tk.END)
    #Field_Strength_Entry.insert(0, str(0))
    
    Field_Direction_Entry.delete(0, tk.END)
    Field_Direction_Entry.insert(0, str(0))
    
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
    Gauge.delete(Pointer)

    
    
    
    #End Data Capture
    end = time.time()
    end_time_list.append(end)
    Elapsed_Time = round(end_time_list[0] - start_time_list[0],2)
    
    
    Data_Vector = [Field_Mag, Field_Angle, Elapsed_Time]
    Data_Vector_List.append(Data_Vector)
    #Text_Box.insert(tk.END, str(Data_Vector)+"\n")
    Text_Box.see("end")
    end_time_list.clear()
    start_time_list.clear()
    
    
    
    
   
    

#Field Strength Input Fields
Field_Strength_Label = tk.Label(text = "Field Strength\n(mT)", borderwidth = 5)
Field_Strength_Label.grid(row = 0, column = 0)
Field_Strength_Entry = tk.Entry(master = window, borderwidth = 5, width =5, font = "24")
Field_Strength_Entry.grid(row = 0, column = 1,sticky = "nswe")

#Field Angle Input Fields
Field_Direction_Label = tk.Label(text = "Field Direction\n(deg)")
Field_Direction_Label.grid(row = 1, column = 0)
Field_Direction_Entry = tk.Entry(master = window, borderwidth = 5, width = 5, font = "24")
Field_Direction_Entry.grid(row = 1, column = 1,sticky = "nswe")

#Zero everything iniitially
Field_Strength_Entry.insert(0,0)
Field_Direction_Entry.insert(0,0)


#Create Apply and Zero Buttons
Apply_Button = tk.Button(master = window,text = "Apply",width = 5,height = 1,
                  fg = "black",bg = "blue", command = Handle_Apply)
Zero_Button = tk.Button(master = window,text = "Zero",width = 5,height = 1,
                  fg = "black",bg = "gray", command = Handle_Zero)

Apply_Button.grid(row=2,column=0,sticky = "nswe")
Zero_Button.grid(row=2,column=1,sticky = "nswe")











#Quick Field Directions
def Handle_Y():
    '''
    MOTOR 1
    need to add the code that will turn the magnetic field on in the Y direction
    '''
    kit.motor1.throttle = float(Duty_Cycle)
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
    Move_Arrow(90)
    print(Duty_Cycle)
    
def Handle_negX():
    '''
    MOTOR 4
    need to add the code that will turn the magnetic field on in the -X direction
    '''
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = float(Duty_Cycle)
    Move_Arrow(180)
    print(Duty_Cycle)
def Handle_X():
    '''
    MOTOR 2
    need to add the code that will turn the magnetic field on in the X direction
    '''
    kit.motor1.throttle = 0
    kit.motor2.throttle = float(Duty_Cycle)
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
    Move_Arrow(0)
    print(Duty_Cycle)
def Handle_negY():
    print("-Y")
    '''
    MOTOR 3
    need to add the code that will turn the magnetic field on in the -Y direction
    '''
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = float(Duty_Cycle)
    kit.motor4.throttle = 0
    Move_Arrow(270)
    print(Duty_Cycle)
    
    
Y_Button = tk.Button(master = window,text = "\u25b2",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black", command = Handle_Y)
negX_Button = tk.Button(master = window,text = "\u25c0",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_negX)
X_Button = tk.Button(master = window,text = "\u25b6",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_X)
negY_Button = tk.Button(master = window,text = "\u25bc",font = "Arial 12",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_negY)
Y_Button.grid(row=0,column=6,sticky = "nswe")
negX_Button.grid(row=1,column=5,sticky = "nswe")
X_Button.grid(row=1,column=7,sticky = "nswe")
negY_Button.grid(row=2,column=6,sticky = "nswe")






#Xbox Controller
def Handle_Xbox():
    Text_Box.insert(tk.END, "XBOX Connected\n")
    #Text_Box.see("end")
    joy = xbox.Joystick() # Instantiate the controller

    # while the back button is 0(i.e not pressed) do all of the below
    while not joy.Back():
        # Left analog stick (x axis range from -1 to 1, y axis range from -1 to 1)
        #to avoid divide by zero error in arctan
        if joy.leftX() == 0 and joy.leftY()  == 0:
            continue
        else:
            Joy_Direction = (180/np.pi)*np.arctan2(joy.leftY() ,joy.leftX())
            Move_Arrow(round(Joy_Direction,2))
            Text_Box.insert(tk.END, str(round(joy.leftX(),2)) + str(round(joy.leftY(),2)) +"\n")
            Text_Box.see("end")
        kit.motor1.throttle = round(joy.leftY(),2)/2  #converging
        kit.motor2.throttle = round(joy.leftX(),2)/2  #converging
        kit.motor3.throttle = -round(joy.leftY(),2)/2 #diverging
        kit.motor4.throttle = -round(joy.leftX(),2)/2 #diverging
        
        # Right trigger range from 0 to 1
        #print("  RightTrg: ", joy.rightTrigger())
        # A/B/X/Y buttons
        #joy.A() == True:
      
        window.update()
            
    #Shut everything down when the back button is pressed
    kit.motor1.throttle = 0  #converging
    kit.motor2.throttle = 0 #converging
    kit.motor3.throttle = 0 #diverging
    kit.motor4.throttle = 0
    joy.close()
    Text_Box.insert(tk.END, "\nXBOX Disconnected")
    Text_Box.see("end")
    
    

    
Xbox_Button = tk.Button(master = window,text = "Xbox Controller",
                  fg = "white",bg = "red",command = Handle_Xbox)
Xbox_Button.grid(row=4,column=0, sticky = "nswe", columnspan = 2)
Stop_Xbox_Label = tk.Label(master = window,text = "To Exit, Press Back Button")
Stop_Xbox_Label.grid(row=5,column=0,sticky = "nswe", columnspan = 2)







#Close Window
def EXIT():
    window.quit()
    window.destroy()
Close_Button = tk.Button(master = window,text = "Close",width = 5,height = 1,
                  fg = "white",bg = "black",command = EXIT)
Close_Button.grid(row=rows[7], column = columns[7], sticky = "nswe")


window.mainloop()


print(Data_Vector_List)

'''
frame = tk.Frame(master = window,
                  width = 150,
                  height = 150,
                  relief = tk.RAISED,
                  borderwidth = 5)
frame.pack(fill = tk.BOTH, side = tk.TOP, expand = True)
label1 = tk.Label(text = "Frame 1",
                  width = 10,
                  height = 10,
                  fg = "green",
                  bg = "red",
                  master = frame1)
label1.grid(row =0, column = 0, sticky = 'ne')
'''

                                                                                                               


