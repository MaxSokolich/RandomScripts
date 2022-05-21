#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:29:43 2022

@author: bizzarohd
"""

import tkinter as tk

import numpy as np



window = tk.Tk() #initilize a window
window.title("MagneticFieldGui")


# get the screen dimension
#screen_width = window.winfo_screenwidth()
#screen_height = window.winfo_screenheight()

window.geometry("800x480")


rows = [0,1,2,3,4,5,6,7]
columns = [0,1,2,3,4,5,6,7]
window.columnconfigure(rows, minsize=100)
window.rowconfigure(columns, minsize = 60)

for i in range(len(rows)):
    for j in range(len(columns)):
        frame = tk.Frame(master = window,
                          width = 100,
                          height = 60,
                          relief = tk.RAISED,
                          borderwidth = 5)
        frame.grid(row = rows[i], column = columns[j])
        
        
#Field Strength and Direction
def Handle_Apply():   
    '''
    need to add the code that will turn on each coil that represents the proper duty cycle.
    '''
    FieldMag = float(Field_Strength_Entry.get())
    FieldAngle = float(Field_Direction_Entry.get())
    
   
    X_Duty_Cycle = FieldMag * np.cos(FieldAngle * np.pi/180)
    Y_Duty_Cycle = FieldMag * np.sin(FieldAngle * np.pi/180)
    print([X_Duty_Cycle, Y_Duty_Cycle])
    
def Handle_Zero():
    FieldVector = [0,0]
    '''
    need to add the code that will turn off all signals to ALL electromagnetic coils
    '''
    print(FieldVector)
    

#Field Strength Input Fields
Field_Strength_Label = tk.Label(text = "Field Strength (mT)", borderwidth = 5)
Field_Strength_Label.grid(row = 0, column = 0)
Field_Strength_Entry = tk.Entry(master = window, borderwidth = 5, width =5)
Field_Strength_Entry.grid(row = 0, column = 0,sticky = "nswe")

#Field Angle Input Fields
Field_Direction_Label = tk.Label(text = "Field XY Direction (deg)")
Field_Direction_Label.grid(row = 1, column = 0)
Field_Direction_Entry = tk.Entry(master = window, borderwidth = 5, width = 5)
Field_Direction_Entry.grid(row = 1, column = 0,sticky = "nswe")

Apply_Button = tk.Button(master = window,text = "Apply",width = 5,height = 1,
                  fg = "black",bg = "blue", command = Handle_Apply)
Zero_Button = tk.Button(master = window,text = "Zero",width = 5,height = 1,
                  fg = "black",bg = "gray", command = Handle_Zero)

Apply_Button.grid(row=0,column=1,sticky = "nswe")
Zero_Button.grid(row=0,column=2,sticky = "nswe")















#Quick Field Directions
def Handle_Y():
    print("Y")
    '''
    need to add the code that will turn the magnetic field on in the Y direction
    FieldMag = float(Field_Strength_Entry.get())
    FieldAngle = 90
    
    '''
    
def Handle_negX():
    print("-X")
    '''
    need to add the code that will turn the magnetic field on in the -X direction
    FieldMag = float(Field_Strength_Entry.get())
    FieldAngle = 180
    '''
def Handle_X():
    print("X")
    '''
    need to add the code that will turn the magnetic field on in the X direction
    FieldMag = float(Field_Strength_Entry.get())
    FieldAngle = 0
    
    '''
def Handle_negY():
    print("-Y")
    '''
    need to add the code that will turn the magnetic field on in the -Y direction
    FieldMag = float(Field_Strength_Entry.get())
    FieldAngle = -270
    '''
    
Y_Button = tk.Button(master = window,text = "Y",width = 5,height = 1,
                  fg = "white",bg = "black", command = Handle_Y)
negX_Button = tk.Button(master = window,text = "-X",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_negX)
X_Button = tk.Button(master = window,text = "X",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_X)
negY_Button = tk.Button(master = window,text = "-Y",width = 5,height = 1,
                  fg = "white",bg = "black",command = Handle_negY)
Y_Button.grid(row=0,column=6,sticky = "nswe")
negX_Button.grid(row=1,column=5,sticky = "nswe")
X_Button.grid(row=1,column=7,sticky = "nswe")
negY_Button.grid(row=2,column=6,sticky = "nswe")























#Xbox Controller
def Handle_Xbox():
    print("Xbox Controller Connected")
def Stop_Xbox():
    print("Xbox Controller Disconnected")
Xbox_Button = tk.Button(master = window,text = "Xbox \nController",
                  fg = "white",bg = "red",command = Handle_Xbox)
Xbox_Button.grid(row=4,column=0, sticky = "nswe", columnspan = 2)
Stop_Xbox_Button = tk.Button(master = window,text = "Stop Xbox\nController",
                  fg = "white",bg = "purple",command = Stop_Xbox)
Stop_Xbox_Button.grid(row=5,column=0,sticky = "nswe", columnspan = 2)






#Update Commands in a text box




#Close Window
def EXIT():
    window.quit()
    window.destroy()
Close_Button = tk.Button(master = window,text = "Close",width = 5,height = 1,
                  fg = "white",bg = "black",command = EXIT)
Close_Button.grid(row=rows[-1], column = columns[-1],sticky = "nswe")


window.mainloop()


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























