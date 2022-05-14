#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:17:01 2021

@author: bizzaro
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation





x0 = 0.01106655
y0 = 0.03922218
t0=0
t1=0.1
t2 = 0.5

xdata = []
ydata = []


def path_until_t(x, x_p, y_p, t_s, t):
    x = -np.cos(time)+np.cos(t0) + x0 
    y = y0 + time-t0
    return x,y

# pathline 
xp =  0.01106655
yp =  0.03922218
x = np.linspace(0,1.0,100)
y2 = yp -  np.arccos(x + np.cos(1.0) - xp) + 1.0

#streakline

#xxx,yyy = path_until_t(x, xp, yp, 0.1,t)

plt.plot(x,y2,'k', label="streak at t = 1, for p ")



def xfield(x0,y0,t0,time):
    #return x0*np.exp(time-t0)
    return  -np.cos(time) + x0 + 1
def yfield(x0,y0,t0,time):
    #return y0*np.exp((-1/2)*(time**2-t0**2))
    return y0 +time

def path(x, x_p, y_p):
    y = y_p + np.arccos(-x +x_p+1)
    return y


fig = plt.figure()

t = np.linspace(0,1,10)# 4 time instances for a single particle
p = np.linspace(0,2,10)# now we want mulitple particles

xp = []
yp = []

xp1 = []
yp1 = []

x_s = []
y_s = []

x_s1 =[]
y_s1 = []

for time in t:
    x = -np.cos(time)+np.cos(t0) + x0 
    y = y0 +time-t0
    yp.append(y)
    xp.append(x)

for time in t:
    x = -np.cos(time)+np.cos(t1) + x0 
    y = y0 +time-t1
    yp1.append(y)
    xp1.append(x) 

tf = 1
for particle in p:
        xs1 = -np.cos(tf)+np.cos(particle) + x0 
        ys1 = y0 +tf-particle
        x_s1.append(xs1)
        y_s1.append(ys1)
'''
#7.389 @t=0
#2.718 @t=1
print("xp = ",xp, "\n")
print("xs = ",x_s)
'''
'''
for p in particles:
    x_s= xfield(x0,y0,p,2)
    y_s = yfield(x0,y0,p,2)
    xs.append(x_s)
    ys.append(y_s)

print(xfield(x0,y0,t0,0.5))
print(xfield(x0,y0,t0,1))
'''
streaktf =2
f = (xfield(1,8,0,streaktf),xfield(1,8,0.33,streaktf),xfield(1,8,0.66,streaktf),xfield(1,8,1,streaktf))

g = (yfield(1,8,0,streaktf),yfield(1,8,0.33,streaktf),yfield(1,8,0.66,streaktf),yfield(1,8,1,streaktf))
print(f,g)
#7.389


plt.plot(xp, yp)
plt.plot(xp1, yp1)
plt.plot(x_s, y_s)
plt.plot(x_s1, y_s1)
plt.xlim(-0.2,.6)
plt.ylim(-0.40,1.2)

plt.show()


