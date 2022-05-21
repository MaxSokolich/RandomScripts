#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 18:45:20 2021

@author: bizzaro
"""

#Quiver


from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation


#Quiver Initals
Initial_Time = 0
Final_Time = 2
streaktf = Final_Time

#axis format
Xaxis = 10
Yaxis = 10
NumVectors = 20


intervals  = 100 #how quickly in ms the plots update

#other initials
#axis format

NumVectors = 20
x = np.linspace(-10,Xaxis, NumVectors)
y = np.linspace(-10
                
                
                
                
                ,Yaxis, NumVectors)
X,Y = np.meshgrid(x,y)

t = np.linspace(Initial_Time,Final_Time, 200)
timespan_q = range(0,len(t))


def ufield(x,y,t):
    return x

def vfield(x,y,t):
    return -y*t



def update_quiver(j, ax, fig):
    u = ufield(X,Y,t[j])
    v = vfield(X,Y,t[j])
    Q.set_UVC(u, v)
    ax.set_title('$t$ = '+ str(round(t[j],3)),fontsize = 26)
    return Q,

def init_quiver():
    global Q
    u = ufield(X,Y,t[0])
    v = vfield(X,Y,t[0])
    Q = ax.quiver(X, Y, u, v)
    
    return  Q,


fig = plt.figure()
ax = plt.subplot()
#ax = fig.gca()
ax.set_title('$t$ = '+ str(t[0]))
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(0,Xaxis)
ax.set_ylim(0,Yaxis)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")




quiv = animation.FuncAnimation(fig, update_quiver, frames = timespan_q,init_func=init_quiver,interval=intervals,fargs=(ax, fig),repeat =False)


plt.axis('equal')
plt.show()
