#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 18:52:46 2022

@author: bizzarohd
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from scipy.integrate import solve_ivp



#pathline
"""
dxp/dt = up(xp(t), t)
xp(t0) = xp0
"""


#vel field
def velocity(t,xy):
    x = xy[0]
    y = xy[1]
    dydt = x+t
    
    dxdt = -y
    return dydt,dxdt



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
  


    xyp0 = [0,1] #path line intial starting point


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
    