#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 14:51:27 2021

@author: bizzaro
"""

import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import random 
import numpy as np

fig = plt.figure()
ax1 = plt.axes()
line, = ax1.plot([], [], lw=2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plotlays, plotcols = [2], ["black","red"]
lines = []
for index in range(2):
    lobj = ax1.plot([],[],lw=2,color=plotcols[index])[0]
    ax1.set_xlim(0,10)
    ax1.set_ylim(0,10)
    lines.append(lobj)


def init():
    for line in lines:
        line.set_data([],[])
    return lines

x1,y1 = [],[]
x2,y2 = [],[]

# fake data
frame_num = 100


def xfield(x0,y0,t0,time):
    return x0*np.exp(time-t0)

def yfield(x0,y0,t0,time):
    return y0*np.exp((-1/2)*(time**2-t0**2))

y0=8
t0=0
    
def animate(i):

    x = xfield(1,y0,t0,i)
    y = yfield(1,y0,t0,i)
    x1.append(x)
    y1.append(y)

    x = xfield(2,y0,t0,i)
    y = yfield(1,y0,t0,i)
    x2.append(x)
    y2.append(y)

    xlist = [x1, x2]
    ylist = [y1, y2]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 

    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frame_num, interval=1000, blit=True)


plt.show()