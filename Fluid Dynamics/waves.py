#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:41:57 2021

@author: bizzaro
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import solve_ivp

fig = plt.figure()
ax = plt.subplot()

plt.xlim(-10, 10)
plt.ylim(-10, 10)

###########################3
a = .5

wavelength = 20 #m

h = 1000

inital_time = 0
final_time = 100
##############################


k = (2*np.pi)/wavelength
g = 9.8
w = np.sqrt(g*k*np.tanh(k*h))

xz0 = [1,1]#path line intial starting point


XQ = np.linspace(-10, 10, 20)
ZQ = np.linspace(-10,10, 20)
xx,zz = np.meshgrid(XQ, ZQ)


u = (a * w * np.cosh(k*(ZQ+h))*np.cos(k*XQ-w*3))/(np.sinh(h*k))
v = (a * w * np.sinh(k*(ZQ+h))*np.sin(k*XQ-w*3))/(np.sinh(h*k))
#plt.quiver(xx,zz,u,v)
#plt.streamplot(xx,zz,u,v)


###General
'''
#dxdt = (a * w * np.cosh(k*(z+h))*np.cos(k*x-w*t))/(np.sinh(h*k))
#dzdt = (a * w * np.sinh(k*(z+h))*np.sin(k*x-w*t))/(np.sinh(h*k))

w = np.sqrt(g*k*np.tanh(k*h))
'''
###DEEP WATER
'''
kh >> 1
 --> w = np.sqrt(g*k)
 --> tan(kh) ~ 1
 --> np.cosh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
 --> np.sinh(k*(z+h)/(np.sinh(h*k)) ~ e^kz

dxdt = a*w*np.exp(k*z)*np.cos(k*x-w*t)
dzdt = a*w*np.exp(k*z)*np.sin(k*x-w*t)
'''



###SHALLOW WATER
'''
 --> w = np.sqrt(g*H*k)
 --> tan(kh) ~ 1
 --> np.cosh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
 --> np.sinh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
 
dxdt = ((a*w)/(k*h))*np.cos(k*x-w*t)
dzdt = a*w(1+(z/h))np.sin(k*x-w*t)

'''



def velocity(t,xy):
    x = xz0[0]
    z = xz0[1]
    dxdt = (a * w * np.cosh(k*(z+h))*np.cos(k*x-w*t))/(np.sinh(h*k))
    dzdt = (a * w * np.sinh(k*(z+h))*np.sin(k*x-w*t))/(np.sinh(h*k))
    
    
    return dxdt,dzdt



  
itv = 100



#path
tspan_p=[inital_time, final_time] #pathline time span region
t_eval_p = np.linspace(inital_time,final_time ,itv) # how many points scipy integrate will evaulte
sol_p = solve_ivp(velocity, tspan_p, xz0, t_eval = t_eval_p)
posx = sol_p.y[0,:]
posz = sol_p.y[1,:]

#solve the equations for xp and yp
#pathline

def init_path():
        global line1
        line1, = plt.plot(posx[0],posz[0], 'o-',markersize=10)
       
        return  line1,
    
def update(i):
       
        
        line1.set_xdata(posx[i:i+1])
        line1.set_ydata(posz[i:i+1])
        
        
        
        return line1,

#height
        

    
#ani = animation.FuncAnimation(fig, update, init_func=init_path,frames=range(0,len(t_eval_p)),interval=100,repeat =True)
#plt.axhline(y=-h, color='r', linestyle='-')
plt.autoscale()
plt.plot(posx,posz)
#plt.plot(u,v)
plt.show()



# %%

#%%
