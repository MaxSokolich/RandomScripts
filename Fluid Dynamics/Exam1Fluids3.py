#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 14:25:03 2021

@author: bizzaro
"""


# %%

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sympy as sp
x, y, z, u, v, w, t = sp.Symbols("x y z u v w t")

Point = (1,0,0)
Time = 2
circulation = 10

x0 = 0
y0 = 1

u = x+t
v = -y

#u = x
#v= -y*t
w = 0

print("Time = ",Time)


ax = sp.diff(u,t) + (u * sp.diff(u,x)) + (v * sp.diff(u,y)) + (w * sp.diff(u,z))
ay = sp.diff(v,t) + (u * sp.diff(v,x)) + (v * sp.diff(v,y)) + (w * sp.diff(v,z))
az = sp.diff(z,t) + (u * sp.diff(z,x)) + (v * sp.diff(z,y)) + (w * sp.diff(z,z))



sp.simplify(ax)
sp.simplify(ay)
sp.simplify(az)

#sp.pprint(ax, "\n")
#sp.pprint(ay,"\n")
#sp.pprint(az,"\n")


axmag=ax.subs(x,Point[0]).subs(y,Point[1]).subs(z,Point[2]).subs(t,Time)
aymag=ay.subs(x,Point[0]).subs(y,Point[1]).subs(z,Point[2]).subs(t,Time)
azmag=az.subs(x,Point[0]).subs(y,Point[1]).subs(z,Point[2]).subs(t,Time)
print("Acceleration in X:")
sp.pprint(axmag)
print("Acceleration in Y:")
sp.pprint(aymag)
print("Acceleration in Z:")
sp.pprint(azmag)

fig = plt.figure()
ax = plt.subplot()
xaxis = [-10,10]
yaxis = [-10,10]
plt.xlim(xaxis[0], xaxis[1])
plt.ylim(yaxis[0], yaxis[1])

#initials
circulation  = 10 #m/s
x0 = 0
y0 = 0
V = 3
alpha = 0

#u0 = V *np.cos(alpha)*x + V *np.sin(alpha)*y

#quiver
def quiver():
    ttt = 1
    V = 1
    alpha = 0

    xvector = np.linspace(xaxis[0], xaxis[1], 20)
    yvector = np.linspace(yaxis[0],yaxis[1], 20)
    
    x,y = np.meshgrid(xvector, yvector)
    
    u = x+ttt#+(-circulation *(y-y0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))
    v = -y#+(circulation *(x-x0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))
    
    ax.quiver(x,y,u,v)
    plt.xlim(xaxis[0], xaxis[1])
    plt.ylim(yaxis[0], yaxis[1])
    
    plt.title('quiver')
 


#streamline
def streamline(t):
    
    start = [[0,1]]
    xvector = np.linspace(xaxis[0], xaxis[1], 10)
    yvector = np.linspace(yaxis[0],yaxis[1], 10)
    x,y = np.meshgrid(xvector, yvector)
    u = x+t#+(-circulation *(y-y0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))
    v = -y#+(circulation *(x-x0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))
    speed = np.sqrt(u*u + v*v)
    
    ax.streamplot(x, y, u, v,start_points=start)#density=(1,1), color=u,linewidth=2*speed)
    
quiver()

streamline(1)
streamline(2)

# %%





#vel field
def velocity(t,xy):
    x = xy[0]
    y = xy[1]
    dydt = x+t
    
    dxdt = -y
    return dydt,dxdt







#pathline
"""
dxp/dt = up(xp(t), t)
xp(t0) = xp0
"""
def pathline():
    global xp
    global yp
    global final_time
    global start_dye
    global end_dye
    global itv
    
    
    inital_time = 0
    final_time = 60 #problem statment
    itv = 10
  


    xyp0 = [0,1]#path line intial starting point


    tspan_p=[inital_time, final_time] #pathline time span region
    
    t_eval_p = np.linspace(inital_time,final_time ,itv) # how many points scipy integrate will evaulte
    
    sol_p = solve_ivp(velocity, tspan_p, xyp0, t_eval = t_eval_p)
     #solve the equations for xp and yp
    
    
    xp = sol_p.y[0,:]
    yp = sol_p.y[1,:]
    
  
    plt.plot(xp,yp, linewidth =2, color = 'black')
    plt.plot(xp[0],yp[0],'go',label='start')
    plt.plot(xp[-1],yp[-1],'ro',label='end')

    plt.legend()
    plt.title('pathline')
