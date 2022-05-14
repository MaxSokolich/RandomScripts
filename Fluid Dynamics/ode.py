#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:17:20 2021

@author: bizzaro
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = plt.subplot()


circulation  = 10 #m/s
x0 = -5
y0 = 0
def velocity(t,xyp0):
    x = xyp0[0]
    y = xyp0[1]
    dypdt = (-circulation *(y-y0))/(2*np.pi*((x-x0)**2+(y-y0)**2))
    
    dxpdt = (circulation *(x-x0))/(2*np.pi*((x-x0)**2+(y-y0)**2))
    return dypdt,dxpdt

'''
scipy.integrate.solve_ivp(fun, t_span, y0, method='RK45', t_eval=None, 
dense_output=False, events=None, vectorized=False, args=None, **options)


t_span = integratoin bounds . t1 -> tf
t_eval = how many points you want to evaluate (an array)

'''
xaxis = [-10,10]
yaxis = [-10,10]

wack = [-4,-3,-2,-1,0,1,2,3,4,5,6]

final_time_streak = 10

track_particle_over_time = 10

xyp0 = [1,0]#path line intial starting point

#quiver




#streamline

xvector = np.linspace(xaxis[0], xaxis[1], 20)
yvector = np.linspace(yaxis[0],yaxis[1], 20)
x,y = np.meshgrid(xvector, yvector)

u = (-circulation *(y-y0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))
v = (circulation *(x-x0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))

speed = np.sqrt(u*u + v*v)


ax.streamplot(x, y, u, v,density=(1,1), color=u,linewidth=5*speed/speed.max())


#pathline
"""
dxp/dt = up(xp(t), t)
xp(t0) = xp0
"""







tspan_p=[0, track_particle_over_time] #pathline time span region
t_eval_p = np.linspace(0,track_particle_over_time ,100) # how many points scipy integrate will evaulte
sol_p = solve_ivp(velocity, tspan_p, xyp0, t_eval = t_eval_p)
 #solve the equations for xp and yp


xp = sol_p.y[0,:]
yp= sol_p.y[1,:]

ax.plot(xp,yp, linewidth =6, color = 'b')






########################################################################################
#streakline



 #the elapsed time after the particle passes thru dye injection,t0 < t_elapsed < tf


elapsed_time_from_passing_thru_dye_source = np.linspace(0,final_time_streak,500) 


#we will loop through each of those time instances where the particle passes thru the 
#injection point, and then solve for there final position at that time
final_p_list_x = []
final_p_list_y = []

for elapsed_time in elapsed_time_from_passing_thru_dye_source:
    
    tspan_s = [elapsed_time,final_time_streak]
    t_eval_p = np.linspace(0,final_time_streak ,20)
    
    #since we have a moving dye source, our intial injection of dye will change with time
    #so we have to acount for that with our inital condition
    
    xys0 = [-4+elapsed_time,0] #(dye_injection_x, dye_injection_y)
    
    
    sol_s = solve_ivp(velocity, tspan_s, xys0)
    tp = sol_s.t
    final_position_x = sol_s.y[0,-1]
    final_position_y = sol_s.y[1,-1]
    final_p_list_x.append(final_position_x)
    final_p_list_y.append(final_position_y)



ax.plot(final_p_list_x,final_p_list_y,linewidth =3, color = 'r')
#########################################################################3
'''
Animations
'''
intervals = 100
#moving dye

dyex = []
dyey = []


t = np.linspace(0,10, 100)

line1, = ax.plot(dyex, dyey, 'o',color='black',markerfacecolor='black')
line2, = ax.plot(xp[0],yp[0], 'ro-')

def dye(t):
    x = -4+t
    y = 0
    dyex.append(x)
    dyey.append(y)
    line1.set_data(dyex, dyey)
    

    line2.set_data(xp[t:t+1],yp[t:t+1])
 
    plt.title('$t$ = '+ str(round(t,1)),fontsize = 26)
    
    return line1,line2
timer = range(0,len(t))




#linep, = ax.plot(xp[0],yp[0], 'ro-')





#ani = FuncAnimation(fig, update, frames=100, interval=intervals,repeat =False)
dye = FuncAnimation(fig, dye, frames=100, interval=intervals,repeat =False)


plt.show()
#################################
######################################################################
plt.xlim(xaxis[0], xaxis[1])
plt.ylim(xaxis[0], xaxis[1])
plt.legend(('pathline','steakline'))
plt.title('two first order ode')
plt.show()












