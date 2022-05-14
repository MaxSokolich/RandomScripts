#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:28:47 2021

@author: bizzaro
"""

from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation



Initial_Time = 0
Final_Time = 5

NumVectors = 20
def ufield(x,y,t):
    return x

def vfield(x,y,t):
    return -y*t

x = np.linspace(0,10, num=NumVectors)
y = np.linspace(0,2, num=NumVectors)
X,Y = np.meshgrid(x,y)

t = np.linspace(Initial_Time,Final_Time,50)

def update_quiver(time, ax, fig):
    u = ufield(X,Y,t[time])
    v = vfield(X,Y,t[time])
    Q.set_UVC(u, v)
    ax.set_title('$t$ = '+ str(t[time]))
    return Q,

def init_quiver():
    global Q
    u = ufield(X,Y,t[0])
    v = vfield(X,Y,t[0])
    Q = ax.quiver(X, Y, u, v)
    ax.set_title('$t$ = '+ str(t[0]))
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    return  Q,

fig = plt.figure()
ax = fig.gca()
ax.set_title('$t$ = '+ str(t[0]))
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(0,10)
ax.set_ylim(0,2)

ts= range(0,len(t))

ani = animation.FuncAnimation(fig, update_quiver, frames = ts,
                              init_func=init_quiver,
                              interval=100,fargs=(ax, fig),repeat = False)
plt.show()

