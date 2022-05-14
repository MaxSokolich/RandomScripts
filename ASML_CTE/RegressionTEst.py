# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 14:06:28 2021

@author: msokolic
"""

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd



"""
y1 mean cte = 0.021
y2 mean cte = -.03

"""
scte = 0.21
scte2 = -0.03
data = pd.read_excel("file:///C:/Users/msokolic/Desktop/Riley Project/ZerodurCurveGeneration.xlsx", sheet_name="data", skiprows = 0)



x = data['xi'].to_numpy()
y1 = data['y1'].to_numpy()
y2 = data['y2'].to_numpy()



def func(x, a, b, c, d, e):
    
    y = a*x+b*x**2+c*(x-scte)**3+d*(x-scte)**4+e*(x-scte**4)*2
    
    return y
    
x1 =-1.98313411e-01  

x2 = 3.16726595e-02 

x3 = 7.33380491e-04

x4 =  -1.44288685e-05
  
x5 = 1.00000000e+00

popt1 , pcov1 = curve_fit(func, x, y1)

print(popt1)


g = func(x, popt1[0], popt1[1], popt1[2], popt1[3], popt1[4])


plt.figure(figsize = (10,8))
plt.plot(x, y1, 'b.')
plt.plot(x, y2, 'r.')
plt.plot(x, g , 'y.')
plt.plot(x,popt1[0]*x+popt1[1]*x**2+popt1[2]*x**3+popt1[3]*x**4+popt1[4]*(x-scte2)*2, 'g.')




plt.xlabel('Temp')
plt.ylabel('TE')
plt.show()

