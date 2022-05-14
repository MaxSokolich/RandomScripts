import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import matplotlib.animation as animation


circulation  = 10 #m/s
x0 = -5
y0 = 0



final_time_streak = 10

track_particle_over_time = 100

xyp0 = [2,0]#path line intial starting point

def velocity(t,xyp0):
    x = xyp0[0]
    y = xyp0[1]
    dypdt = (-circulation *(y-y0))/(2*np.pi*((x-x0)**2+(y-y0)**2))
    
    dxpdt = (circulation *(x-x0))/(2*np.pi*((x-x0)**2+(y-y0)**2))
    return dypdt,dxpdt


tspan_p=[0, track_particle_over_time] #pathline time span region
t_eval_p = np.linspace(0,track_particle_over_time ,200) # how many points scipy integrate will evaulte
sol_p = solve_ivp(velocity, tspan_p, xyp0, t_eval = t_eval_p)
 #solve the equations for xp and yp


xp = sol_p.y[0,:]
yp= sol_p.y[1,:]




fig, ax = plt.subplots()
line, = ax.plot(1,7, 'ro-')


ax.set_xlim(-15,15)
ax.set_ylim(-15,15)

def update(i):
    new_data1 = xp[:i]
    new_data2 = yp[:i]
    line.set_xdata(new_data1)
    line.set_ydata(new_data2)
    return line,

ani = animation.FuncAnimation(fig, update, frames=track_particle_over_time, interval=100)
plt.show()