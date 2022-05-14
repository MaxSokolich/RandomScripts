#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 14:46:26 2021

@author: bizzaro
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

fig = plt.figure()


######################################################################
#define pathline function containing velocity fields
def path(t,xyp0):
    x = xyp0[0]
    y = xyp0[1]
    dypdt = x
    
    dxpdt = -y*t
    return dypdt,dxpdt


xyp0 = [1,8] #path line intial starting point
tspan_p=[0,2] #pathline time span region
t_eval_p = np.linspace(0,2,200) # how many points scipy integrate will evaulte


sol_p = solve_ivp(path, tspan_p, xyp0, t_eval = t_eval_p) #solve the equations for xp and yp

tp = sol_p.t
xp = sol_p.y[0,:]
yp= sol_p.y[1,:]

plt.plot(xp,yp, linewidth =6)
plt.legend(('y(t)','x(t)'))
plt.title('two first order ode')

#7.389318862953665
#1.083630331050105
######################################################################
"""

 
 the elapsed time after the particle passes thru dye injection,t0 < t_elapsed < tf
"""
final_time = 2
elapsed_time_from_passing_thru_dye_source = np.linspace(0,final_time,50) 

final_p_list_x = []
final_p_list_y = []

'''
we will loop through each of those time instances where the particle passes thru the 
injection point, and then solve for there final position at that time
'''
for elapsed_time in elapsed_time_from_passing_thru_dye_source:
    def streak(t,xys):
        x = xys[0]
        y = xys[1]
        dysdt = x 
        
        dxsdt = -y*t
        return dysdt,dxsdt
    tspan_s = [elapsed_time,final_time]
    xys = [1,8] #(dye_injection_x, dye_injection_y)
    
    
    sol_s = solve_ivp(streak, tspan_s, xys)
    tp = sol_s.t
    final_position_x = sol_s.y[0,-1]
    final_position_y = sol_s.y[1,-1]
    final_p_list_x.append(final_position_x)
    final_p_list_y.append(final_position_y)



plt.plot(final_p_list_x,final_p_list_y)



#
######################################################################
plt.xlim(0,10)
plt.ylim(0,10)
plt.legend(('y(t)','x(t)'))
plt.title('two first order ode')
plt.show()
