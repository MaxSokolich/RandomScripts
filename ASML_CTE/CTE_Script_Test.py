# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



#trendline equation to latex format function
def poly2latex(poly, variable="x", width=5):
    t = ["{0:0.{width}f}"]
    t.append(t[-1] + " {variable}")
    t.append(t[-1] + "^{1}")

    def f():
        for i, v in enumerate(reversed(poly)):
            idx = i if i < 2 else 2
            yield t[idx].format(v, i, variable=variable, width=width)

    m="{}".format("+".join(f()))
    #print(m)
    

from sympy import S, symbols, printing
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from shapely.geometry import LineString

#ULE Data Extraction
try:
    LU_Val = 541
    NU_Val = 347
    HU_Val = 153
    LZ_Val = 588
    NZ_Val = 1.8
    HZ_Val = 235
    #Data Extraction: read excel file
    
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
        TE_LZ = 10**6*((-3.4703*10**-18)*i**6/6+0.0000000000000014695*i**5/5+-0.000000000000056999*i**4/4+(-2.368565364*10**-11)*i**3/3+0.00000000153887*i**2/2+0.00000001093*i  + 0.000000128)
        LowZ.append(TE_LZ)
        
    for i in TempRange:
        TE_HZ = 10**6*((-3.4703*10**-18)*i**6/6+0.0000000000000014695*i**5/5+-0.000000000000056999*i**4/4+(-2.368565364*10**-11)*i**3/3+0.00000000153887*i**2/2+0.00000001093*i  - 0.000000695)
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
      
    print(NominalULE)
    ULE_Nominal_Line= LineString(np.column_stack((TempRange, NominalULE)))
    Z_Nominal_Line= LineString(np.column_stack((TempRange, NominalZ)))
    N_intersection = ULE_Nominal_Line.intersection(Z_Nominal_Line)
    
    #Low intersection points
    ULE_Low_Line= LineString(np.column_stack((TempRange, LowULE)))
    Z_Low_Line= LineString(np.column_stack((TempRange, LowZ)))
    L_intersection = ULE_Low_Line.intersection(Z_Low_Line)
    
    #high intersection points
    ULE_High_Line= LineString(np.column_stack((TempRange, HighULE)))
    Z_High_Line= LineString(np.column_stack((TempRange, HighZ)))
    H_intersection = ULE_High_Line.intersection(Z_High_Line)
    
    print(H_intersection)
    
    
    #Trendline of Nominal Data sets
    
    fitZ = pl.polyfit(TempRange, NominalZ, 6)
    TL_Z = np.poly1d(fitZ)
    
    
    eq1 = str(fitZ[0])+"x^6  +  "+str(fitZ[1])+"x^5   +  "+str(fitZ[2])+"x^4  +  "+str(fitZ[3])+"x^3  +  "+str(fitZ[4])+"x^2  +  "+str(fitZ[5])+"x    "+str(fitZ[6])
    
    fitULE = np.polyfit(TempRange, NominalULE, 6)
    TL_ULE = np.poly1d(fitULE)
    
    eq2 = str(fitULE[0])+"x^6  +  "+str(fitULE[1])+"x^5   +  "+str(fitULE[2])+"x^4  +  "+str(fitULE[3])+"x^3  +  "+str(fitULE[4])+"x^2  +  "+str(fitULE[5])+"x    "+str(fitULE[6])
    
    
    
    
    
    
    #intersection points
    
   
    
    def intersectionpoints(intersection):
        points = []
        for p in intersection:
            if p.x >100:
                points.append([p.x, p.y])
    
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
    
            
    #Plot data, figure 1
    plt.rcParams['figure.figsize'] = [10, 8]
    fig, (ax1,ax2) = plt.subplots(2,1,facecolor = "#A0F0CC")
    
    
    ax1.plot(TempRange,NominalULE, color = 'r',label = 'NominalULE')
    ax1.plot(TempRange, LowULE, color = 'b',label = 'LowULE')
    ax1.plot(TempRange, HighULE, color = 'g', label = 'HighULE')
    
    ax1.plot(TempRange,NominalZ, color = 'k',label = 'NominalZ')
    ax1.plot(TempRange, LowZ, color = 'c',label = 'LowZ')
    ax1.plot(TempRange, HighZ, color = 'y', label = 'HighZ')
    
    
    ax1.set_xlim(0)
    ax1.set_ylim(-5)
    ax1.legend()
    
    plotintersectionpoints(intersectionpoints(N_intersection))
    plotintersectionpoints(intersectionpoints(L_intersection))
    plotintersectionpoints(intersectionpoints(H_intersection))
    #plot data, figure 2
    
    ax2.plot(TempRange,NominalULE, color = 'r',label = 'NominalULE', linewidth = 1)
    ax2.plot(TempRange, TL_ULE(TempULE), "r--", label = "Nominal ULE Trendline", linewidth = 2)
    
    ax2.plot(TempRange,NominalZ, color = 'k',label = 'NominalZ', linewidth = 1)
    ax2.plot(TempRange, TL_Z(TempZ), "k--", label = "Nominal Z Trendline", linewidth = 2)
    
    ax2.scatter(array_points[:,0],array_points[:,1])
    for x,y in zip(array_points[:,0],array_points[:,1]):
    
                label = "{:.2f}".format(x),"{:.2f}".format(y)
            
                plt.annotate(label, # this is the text
                             (x,y), # this is the point to label
                             textcoords="offset points", # how to position the text
                             xytext=(0,20), # distance from text to points (x,y)
                             ha='center') # horizontal alignment can be left, right or center
    
    
    ax2.set_xlim(0)
    ax2.set_ylim(-5)
    ax2.legend()
    
    plt.xlabel("Temp [C]")
    ax1.set_ylabel("Thermal Expansion [ppb/C]")
    ax2.set_ylabel("Thermal Expansion [ppb/C]")
    
    plt.show()
    
    
    
    #Display Results
    #tempuratures at which the thermal expansions of Zerodur and ULE match
    TempuratureMatch = []
    for i in points:
        TempuratureMatch.append(str(round(i[0],3)))
                
    print(TempuratureMatch)
    
    #print("ULE Thermal Expansion Trendline Equation: ", eq2)
    #print("Zerodur Thermal Expansion Trendline Equation: ", eq1)


except IOError:
    print("failed")