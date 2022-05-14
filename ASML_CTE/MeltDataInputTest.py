# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 14:26:36 2021

@author: msokolic
"""

import PySimpleGUI as sg
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from shapely.geometry import LineString
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

        
"""
def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    make_dpi_aware()
"""
#Function for drawing
def draw_figure(canvas, figure):
                 
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg



Descrip = """Click --Browse-- to select the Excel File named:\n\n\n   CTE_Data_Test.xlsx \n\n\n Press --Submit--. \n\nA thermal expansion plot,  trendlines, 
and temperature matches for the nominal datasets will be calculated and displayed. \n\nPress --Exit-- to close the app or --New File-- to select another file """


#sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)
#print = sg.Print
font1 = ("Arial", 20)
font2 = ("Arial", 10)
layout = [
        [sg.Text("Enter ULE Melt Data: "), sg.InputText(size=(50, 250), enable_events=True, key = "ULEmelt"),sg.Text("Temperature Match [C]:",font=font1,text_color="white"),sg.Text(size=(20,1), justification='center',text_color='red', background_color='white', key='tempnum',font=("Arial",25))],
        [sg.Text("Enter Zerodur Melt Data: "), sg.InputText(size=(50, 250), enable_events=True, key = "Zmelt")],
        [ sg.Submit() ,sg.Button("Clear"),sg.Button("Exit")],
           
           [sg.Canvas(key="-CANVAS-"),sg.Text(Descrip, size=(25,25), justification='left',text_color='black', background_color='white')],#sg.Listbox(values="Log", size=(40, 1), key='_LISTBOX_')],
            
           [sg.Text("Zerodur Trendline:",font=font2,justification='right'),sg.Text(size=(150,2), justification='left',text_color='black',font=font2, background_color='white', key='eq1')],
           [sg.Text("     ULE Trendline:",font=font2,justification='right'),sg.Text(size=(150,2), justification='left',text_color='black',font=font2, background_color='white', key='eq2')]]
        



    
#window = sg.Window('My File Browser', layout, size=(200,300))

w,h = sg.Window.get_screen_size()
window = sg.Window('Zerodur and ULE CTE Matching GUI', layout, finalize=True, size=(int(w-w*(1/5)),int(h-h*(1/8))),element_justification='left',font='Monospace 12')

plt.rcParams['figure.figsize'] = [11, 7]
fig = Figure()
ax2 = fig.add_subplot(facecolor = "#A0F0CC")
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        
        break
   
    if event == "Clear":
        
        fig = Figure()
        fig_agg.get_tk_widget().pack_forget()
        ax2 = fig.add_subplot(facecolor = "#A0F0CC")
        fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        
        window.FindElement('tempnum').Update("")
        window.FindElement('eq1').Update("")
        window.FindElement('eq2').Update("")
    if event == "Submit":
        try:
            
            
            ULEmelt = int(values['ULEmelt'])
            Zmelt = int(values['Zmelt'])
            """
            
            how to convert tzc and meant CTE values into low, high, nominal values in the equations used
            
            
            
            
            
            
            
            """
            
            
            
            
            LU_Val = (541-ULEmelt)
            NU_Val = (347-ULEmelt)
            HU_Val = (153 - ULEmelt)
            
            LZ_Val = (588-Zmelt)
            NZ_Val = (1.8-Zmelt)
            HZ_Val = (235-Zmelt)
            
            TempRange = list(range(20,285, 5))
            
          
               
            NominalULE = []
            LowULE = []
            HighULE = []
            
            NominalZ = []
            LowZ = []
            HighZ = []
            
            for i in TempRange:
                TE_NU = (0.0000000000014871*(i**7)/7-0.00000000086076*(i**6)/6+0.000000084764*(i**5)/5+0.000039658*(i**4)/4-0.014705*(i**3)/3+2.1035*(i**2)/2-36.5162*i+NU_Val)/1000
                NominalULE.append(TE_NU)
            
            #LowULE
            for i in TempRange:
                TE_LU = (0.0000000000014871*i**7/7-0.00000000086076*i**6/6+0.000000084764*i**5/5+0.000039658*i**4/4-0.014705*i**3/3+(2.1035-0.03)*i**2/2-(36.5162+9.4)*i+LU_Val)/1000
                LowULE.append(TE_LU)
            
            for i in TempRange:
                TE_HU = (0.0000000000014871*i**7/7-0.00000000086076*i**6/6+0.000000084764*i**5/5+0.000039658*i**4/4-0.014705*i**3/3+(2.1035+0.03)*i**2/2-(36.5162-9.4)*i+HU_Val)/1000
                HighULE.append(TE_HU)
                
            for i in TempRange:
                TE_NZ = 10**6*((-3.4703*10**-18)*i**6/6+0.0000000000000014695*i**5/5+-0.000000000000056999*i**4/4+(-2.368565364*10**-11)*i**3/3+0.00000000153887*i**2/2+0.00000001093*i  - 0.00000046)
                NominalZ.append(TE_NZ)
                
            for i in TempRange:
                TE_LZ = 10**6*((-3.452949*10**-18)*i**6/6+0.0000000000000014695*i**5/5+-0.000000000000056999*i**4/4+(-2.368565364*10**-11)*i**3/3+0.0000000013887*i**2/2-0.000000018581*i  + 0.000000128)
                LowZ.append(TE_LZ)
                
            for i in TempRange:
                TE_HZ = 10**6*((-3.4703*10**-18)*i**6/6+0.0000000000000014695*i**5/5+-0.000000000000056999*i**4/4+(-2.39225*10**-11)*i**3/3+0.0000000016158*i**2/2+0.00000002186*i  - 0.000000695)
                HighZ.append(TE_HZ)
            
            
            #print(NominalULE)
            #print(LowULE)
            #print(HighULE)
            
            TempRange = np.array(TempRange)
            
            NominalULE = np.array(NominalULE)
            LowULE = np.array(LowULE)
            HighULE = np.array(HighULE)
            
            NominalZ = np.array(NominalZ)
            LowZ = np.array(LowZ)
            HighZ = np.array(HighZ)    
               
            
            
               #Nominal intersection points
            
            def TrimmedRanges(dataset):
                datasetnew = dataset[36:54]
                return datasetnew
                
            
            
            ULE_Nominal_Line= LineString(np.column_stack((TrimmedRanges(TempRange), TrimmedRanges(NominalULE))))
            Z_Nominal_Line= LineString(np.column_stack((TrimmedRanges(TempRange), TrimmedRanges(NominalZ))))
            N_intersection = ULE_Nominal_Line.intersection(Z_Nominal_Line)
            
            #Low intersection points
            ULE_Low_Line= LineString(np.column_stack((TrimmedRanges(TempRange), TrimmedRanges(LowULE))))
            Z_Low_Line= LineString(np.column_stack((TrimmedRanges(TempRange), TrimmedRanges(LowZ))))
            L_intersection = ULE_Low_Line.intersection(Z_Low_Line)
            
            #high intersection points
            ULE_High_Line= LineString(np.column_stack((TrimmedRanges(TempRange), TrimmedRanges(HighULE))))
            Z_High_Line= LineString(np.column_stack((TrimmedRanges(TempRange), TrimmedRanges(HighZ))))
            H_intersection = ULE_High_Line.intersection(Z_High_Line)
            
            





            
            #Trendline of Nominal Data sets
    
            fitZ = pl.polyfit(TempRange, NominalZ, 6)
            TL_Z = np.poly1d(fitZ)
            
            p = 15#decimal to round equation coefficents to
            eq1 = str(round(fitZ[0],p))+"x^6  +  "+str(round(fitZ[1],p))+"x^5   +  "+str(round(fitZ[2],p))+"x^4  +  "+str(round(fitZ[3],p))+"x^3  +  "+str(round(fitZ[4],p))+"x^2  +  "+str(round(fitZ[5],p))+"x  +  "+str(round(fitZ[6],p))
    
            fitULE = np.polyfit(TempRange, NominalULE, 6)
            TL_ULE = np.poly1d(fitULE)
            
            eq2 = str(round(fitULE[0],p))+"x^6  +  "+str(round(fitULE[1],p))+"x^5   +  "+str(round(fitULE[2],p))+"x^4  +  "+str(round(fitULE[3],p))+"x^3  +  "+str(round(fitULE[4],p))+"x^2  +  "+str(round(fitULE[5],p))+"x  +  "+str(round(fitULE[6],p))
    
            
            
            
            
            #Nominal intersection points
            def intersectionpoints(intersection):
                points = []
                
                points.append([intersection.x, intersection.y])
            
                array_points = np.array(points)
              
                return array_points
            
            def plotintersectionpoints(array_points):
                ax2.scatter(array_points[:,0],array_points[:,1],linewidth = 5)
                for x,y in zip(array_points[:,0],array_points[:,1]):
            
                    label = "{:.2f}".format(x),"{:.2f}".format(y)
            
                    ax2.annotate(label, # this is the text
                             (x,y), # this is the point to label
                             textcoords="offset points", # how to position the text
                             xytext=(60,10), # distance from text to points (x,y)
                             ha='center') # horizontal alignment can be left, right or centerr
            
            intersectionpoints(N_intersection)
            intersectionpoints(L_intersection)
            intersectionpoints(H_intersection)
            
            #Nominal ULE
            ax2.plot(TempRange,NominalULE, color = 'r',label = 'NominalULE', linewidth = 2)
            #ax2.plot(TempULE, TL_ULE(TempULE), "r--", label = "Nominal ULE Trendline", linewidth = 2)
            
            ax2.plot(TempRange, LowULE, color = 'b',label = 'LowULE',linewidth =2)
              
            #HIGH ULE
            ax2.plot(TempRange, HighULE, color = 'g', label = 'HighULE', linewidth  =2)
            
            #Nominal Z
            ax2.plot(TempRange,NominalZ, color = 'k',label = 'NominalZ', linewidth = 2)
            #ax2.plot(TempZ, TL_Z(TempZ), "k--", label = "Nominal Z Trendline", linewidth = 2)
            
            #LOW Z
            ax2.plot(TempRange, LowZ, color = 'c',label = 'LowZ', linewidth=2)
            
            #HIGH Z
            ax2.plot(TempRange, HighZ, color = 'y', label = 'HighZ',linewidth = 2)
            
            plt.show()
            
            
            
            plotintersectionpoints(intersectionpoints(N_intersection))
            plotintersectionpoints(intersectionpoints(L_intersection))
            plotintersectionpoints(intersectionpoints(H_intersection))
            
            ax2.set_xlim(0)
            ax2.set_ylim(-5)
            ax2.legend()
            ax2.grid()
            ax2.set_xlabel("Temp [C]")
            ax2.set_ylabel("Thermal Expansion [ppb/C]")
           
    
            
                   
            fig_agg.draw()
            
            
        
            NTemperatureMatch = round(intersectionpoints(N_intersection)[0][0],3)
           
            
            window.FindElement('tempnum').Update(NTemperatureMatch)
            window.FindElement('eq1').Update(eq1)
            window.FindElement('eq2').Update(eq2)
        
        
        
        
        
        except Exception:
            print("Please Try Again")
            
            layouterror = [[sg.Text("Error.\nPlease Try Again.",font=font1)],[sg.Button("OK",font=font1)]]
            windowerror = sg.Window("Error", layouterror, size = (400,400))
            
            while True:
                event, values = windowerror.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "OK":
                    windowerror.close()
            #Clear window for new data incoming
        
        
    


window.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

