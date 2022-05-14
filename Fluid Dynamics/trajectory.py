#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 10:17:01 2021

@author: bizzaro
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


x0=1
y0=1
t0=0


xdata = []
ydata = []

fig, ax = plt.subplots()
ax.set_xlim(0,10)
ax.set_ylim(0,10)
line, = ax.plot(xdata, ydata, animated = True)

def xfield(x0,y0,t0,time):
    return x0*np.exp(time-t0)

def yfield(x0,y0,t0,time):
    return y0*np.exp((-1/2)*(time**2-t0**2))

def init_an():
    global line
    line, = ax.plot(xdata, ydata)
    return  line,

def update_path(time,ax,fig):
    
	xdata.append(xfield(x0,y0,t0,time))
	ydata.append(yfield(x0,y0,t0,time))
	line.set_data(xdata, ydata)
	return line,


Initial_Time = 0
Final_Time = 1

t = np.linspace(Initial_Time,Final_Time,50)
ts = range(0,len(t))
intervals  = 100



path = animation.FuncAnimation(fig, update_path,frames=t, init_func=init_an, interval = intervals,fargs=(ax, fig),repeat = False)

plt.show()


