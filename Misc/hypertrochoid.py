#---------------------------------------------------------------------------#


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

plt.style.use('dark_background')
#---------------------------------------------------------------------------#

R = 5
r = 3
d = 5

fig = plt.figure()
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10)) 
line, = ax.plot([],[], lw=2)
plt.style.use('dark_background')


def init():
    line.set_data([],[])
    return line,

xdata = []
ydata = []

def animate(i):
    theta = i * 0.01*1.2*np.pi
    x = (R - r)*np.cos(theta) + d*np.cos((R-r)/r*theta)  #float error :(
    y = (R - r)*np.sin(theta) - d*np.sin((R-r)/r*theta)
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata,ydata)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, 
						frames=500, interval=20, blit=True)
plt.xlabel("x = (R - r)*np.cos(theta) + d*np.cos((R-r)/r*theta)")
plt.ylabel("y = (R - r)*np.sin(theta) - d*np.sin((R-r)/r*theta)")
plt.title("Hypertrochoid for 0<theta<  ")
plt.show()





