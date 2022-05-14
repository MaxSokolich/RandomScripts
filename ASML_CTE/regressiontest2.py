# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 10:49:02 2021

@author: msokolic
"""

import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import random

plt.rcParams["figure.figsize"] = (14,12)

data = pd.read_excel("file:///C:/Users/msokolic/Desktop/Riley Project/ZerodurCurveGeneration.xlsx", sheet_name="data", index_col=False)
Temp = data["T"].to_numpy()
High = data["h"].to_numpy()
Nom = data["n"].to_numpy()
Low = data["l"].to_numpy()

scte1 = 0.039
scte2 = 0
scte3 = -0.034

#lp = True
#while lp == True:
for i in range(0,10000000):
    a = random.randint(-300,300)
    b = random.randint(-300,300)
    c = random.randint(-300,300)
    d = random.randint(-300,300)
    e = random.randint(-300,300)
    
    
    print("Regression Step", i)
    def func1(x, A, B, C, D, E):
        global a
        global b
        global c
        global d
        global e
        y =  A*(x+(scte1*a))+   B*(x+(scte1*b))**2+    C*(x+(scte1*c))**3+    D*(x+(scte1*d))**4 +     E*(x+(scte1*e))**5 
        return y
    
    popt1, pcov1 = curve_fit(func1, Temp, High)
    
    A = popt1[0]
    B = popt1[1]
    C = popt1[2]
    D = popt1[3]
    E = popt1[4]
    
    def finaleq(scte,a,b,c,d,e):
        eq = A*(Temp+(scte*a))+   B*(Temp+(scte*b))**2+    C*(Temp+(scte*c))**3+    D*(Temp+(scte*d))**4 +     E*(Temp+(scte*e))**5 
        return eq

    #least Squares
    
    SSQHIGH = []
    SSQNOM = []
    SSQLOW = []
    
    for i in range(len(High)):
        SQH = (High[i]-finaleq(scte1,a,b,c,d,e)[i])**2
        SQN = (Nom[i]-finaleq(scte2,a,b,c,d,e)[i])**2
        SQL = (Low[i]-finaleq(scte3,a,b,c,d,e)[i])**2
        
        SSQHIGH.append(SQH)
        SSQNOM.append(SQN)
        SSQLOW.append(SQL)
        
    ssqn = sum(SSQNOM)
    ssql = sum(SSQLOW)
   
    if ssqn < 20 and ssql < 20:
        break
print(popt1)
print(a,b,c,d,e)
print("stop")
print("SSQ High = ", sum(SSQHIGH))

print("SSQ Nom = ",sum(SSQNOM))

print("SSQ Low = ",sum(SSQLOW))
            

plt.plot(Temp, High, 'r.')
plt.plot(Temp, Nom, 'g.')
plt.plot(Temp, Low, 'b.')
plt.plot(Temp, finaleq(scte1,a,b,c,d,e) , 'r')
plt.plot(Temp, finaleq(scte2,a,b,c,d,e) , 'g')
plt.plot(Temp, finaleq(scte3,a,b,c,d,e), 'b')

plt.show()


