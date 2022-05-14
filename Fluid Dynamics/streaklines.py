#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:51:05 2021

@author: bizzaro
"""
# python code

pl.rcParams["figure.figsize"] = (10,10)
import numpy as np
import matplotlib.pyplot as pl 
np.seterr(invalid='ignore')

#PATHLINE
def path(x, x_p, y_p):
    y = y_p + np.arccos(-x +x_p+1)
    return y

x = np.linspace(0,1.0,100)
#at t = 0, the initial positions are generated at random
x_0 = np.random.rand(4)
y_0 = np.random.rand(4)

#STREAKLINE

def path_until_t(x, x_p, y_p, t_s, t):
    x = x_p - np.cos(t) + np.cos(t_s)
    y = y_p + t - t_s
    return x,y

# pathline 
xp0 =  0.01106655
yp0 =  0.03922218
x = np.linspace(0,1.0,100)
y2 = yp0 -  np.arccos(x + np.cos(1.0) - xp0) + 1.0

#streakline
t = np.linspace(0, 1.0, 30)
#xxx,yyy = path_until_t(x, xp0, yp, 0.1,t)

pl.plot(x,y2,'k', label="streak at t = 1, for p ")






pl.plot(xp0, yp0, 'ro')
pl.plot(x, path(x,xp0,yp0),'b--', label="path starting at t=0, through p")


'''
pl.plot(path_until_t(x, xp0, yp0, 0.1,t)[0], path_until_t(x, xp0, yp0, 0.1,t)[1],'c--', label= "path starting at t=0.1, through p")
pl.plot(path_until_t(x, xp0, yp0, 0.1,t)[0][-1], path_until_t(x, xp0, yp0, 0.1,t)[1][-1],'co')


pl.plot(path_until_t(x, xp0, yp0, 0.2,t)[0], path_until_t(x, xp0, yp0, 0.2,t)[1],'g--', label= "path starting at t=0.2, through p")
pl.plot(path_until_t(x, xp0, yp0, 0.2,t)[0][-1], path_until_t(x, xp0, yp0, 0.2,t)[1][-1],'go')


pl.plot(path_until_t(x, xp0, yp0, 0.5,t)[0], path_until_t(x, xp0, yp0, 0.5,t)[1],'m--', label= "path starting at t=0.5, through p")
pl.plot(path_until_t(x, xp0, yp0, 0.5,t)[0][-1], path_until_t(x, xp0, yp0, 0.5,t)[1][-1],'mo')

'''
pl.xlim(-0.2,0.6)
pl.ylim(-0.5, 1.2)
pl.legend()