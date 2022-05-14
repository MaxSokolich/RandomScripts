#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 21:31:50 2021

@author: bizzaro
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import solve_ivp
plt.rcParams["figure.figsize"] = (10,10)


##############GENERAL
#
# --> w = np.sqrt(g*k*np.tanh(k*h))
#dxdt = (a * w * np.cosh(k*(z+h))*np.cos(k*x-w*t))/(np.sinh(h*k))
#dzdt = (a * w * np.sinh(k*(z+h))*np.sin(k*x-w*t))/(np.sinh(h*k))
#
#
#
##############DEEP WATER
#'''
#kh >> 1
#
# --> w = np.sqrt(g*k)
# --> tan(kh) ~ 1
# --> np.cosh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
# --> np.sinh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
#
#dxdt = a*w*np.exp(k*z)*np.cos(k*x-w*t)
#dzdt = a*w*np.exp(k*z)*np.sin(k*x-w*t)
#
#
#
#
##############SHALLOW WATER
#
#kh<<1
#
# --> w = np.sqrt(g*H*k)
# --> tan(kh) ~ 1
# --> np.cosh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
# --> np.sinh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
# 
#dxdt = ((a*w)/(k*h))*np.cos(k*x-w*t)
#dzdt = a*w(1+(z/h))np.sin(k*x-w*t)
#
#
#
#
#
#
#
#
# %%
fig = plt.figure()
ax = plt.subplot()

ax.set_xlim(-50,50)
ax.set_ylim(-50,50)


Final_Time = 1


a = .5                                                                         #wave amplitudee
wavelength = 20 #m
h = 1000                                                                       #depth of ocean
k = (2*np.pi)/wavelength
g = 9.8
omeg = np.sqrt(g*k*np.tanh(k*h))



x = np.linspace(-10,50, 100)
z = np.linspace(0,20, 100)
X,Z = np.meshgrid(x,z)

t = np.linspace(0,Final_Time, 100)

xz0 = [0,0]                                                                   #path line intial starting point




#%%




xp = []
yp = []

##################33


#plotting actually velocities over time

line1, = ax.plot(xp, yp, "-o")

def animate(i,ax,fig):
    uu = a * omeg * (np.cosh(k*(Z+h))/(np.sinh(h*k)))*np.cos(k*X-omeg*i)
    vv = a * omeg * (np.sinh(k*(Z+h))/(np.sinh(h*k)))*np.sin(k*X-omeg*i)
    xp.append(uu)
    yp.append(vv)
    line1.set_data(uu, vv)
    ax.set_title('$time$ = '+ str(i),fontsize = 26)
    return line1




    

#plt.axhline(y=-h, color='r', linestyle='-')


# %%
velocity = animation.FuncAnimation(fig, animate, frames=t,fargs = (ax,fig), interval=100,repeat = True)





ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")


plt.show()