#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 20:56:52 2021

@author: bizzaro
"""
'''
ani1 = animation.FuncAnimation(fig, update_quiver, frames = range(0,len(t)),
                              init_func=init_quiver,
                              interval=1,fargs=(ax, fig),repeat = False)
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import solve_ivp

#streamplot intials


#Quiver Initals
Initial_Time = 0
Final_Time = 2


xyinitial = [1,8]

intervals  = 100 #how quickly in ms the plots update

#streak

tp1 = 0
tp2 = 0.33
tp3 = .66
tp4 = 1






#Initials

streaktf = Final_Time

#axis format
Xaxis = 8
Yaxis = 8
NumVectors = 20




#other initials

x = np.linspace(0,Xaxis, NumVectors)
y = np.linspace(0,Yaxis, NumVectors)
X,Y = np.meshgrid(x,y)

t = np.linspace(Initial_Time,Final_Time, 200)

timespan_q = range(0,len(t))

#quiver
#################################################################################################################################################################################################################
a = .5

wavelength = 20 #m

h = 1000
k = (2*np.pi)/wavelength
g = 9.8
omeg = np.sqrt(g*k*np.tanh(k*h))


def ufield(x,y,t):
    return x+t

def vfield(x,y,t):
    return -y




def update_quiver(j, ax, fig):
    u = ufield(X,Y,t[j])
    v = vfield(X,Y,t[j])
    Q.set_UVC(u, v)
    ax.set_title('$streak tf$ = '+ str(round(t[j],3)),fontsize = 26)
    
    return Q,

def init_quiver():
    global Q
    u = ufield(X,Y,t[0])
    v = vfield(X,Y,t[0])
    Q = ax.quiver(X, Y, u, v)
    
    return  Q,


fig = plt.figure()
ax = plt.subplot()
#ax = fig.gca()

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(0,Xaxis)
ax.set_ylim(0,Yaxis)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")



def xfield(x0,y0,t0,time):
    return x0*np.exp(time-t0)

def yfield(x0,y0,t0,time):
    return y0*np.exp((-1/2)*(time**2-t0**2))



#################################################################################################################################################################################################################
#streak
    





#7.389318862953665
#1.083630331050105
######################################################################
time = np.linspace(0,2,5)
sx = []
sy = []

for i in time:
    def streak(t,xyp0):
        x = xyp0[0]
        y = xyp0[1]
        dypdt = x
        
        dxpdt = -y*t
        return dypdt,dxpdt
    tspan_s = [i,2]
    xys = [1+i,8]
    
    
    sol_s = solve_ivp(streak, tspan_s, xys)
    tp = sol_s.t
    xsss = sol_s.y[0,-1]
    ysss = sol_s.y[1,-1]
    sx.append(xsss)
    sy.append(ysss)

print(sx)
print(sy)

ax.plot(sx,sy,linewidth = 6)

######################3

firstpath = [xyinitial[0],xyinitial[1],tp1]
secondpath = [xyinitial[0],xyinitial[1],tp2]
thirdpath= [xyinitial[0],xyinitial[1],tp3]
fourthpath = [xyinitial[0],xyinitial[1],tp4]

xs1 = (xfield(xyinitial[0],xyinitial[1],tp1,streaktf),xfield(xyinitial[0],xyinitial[1],tp2,streaktf),xfield(xyinitial[0],xyinitial[1],tp3,streaktf),xfield(xyinitial[0],xyinitial[1],tp4,streaktf))

ys1 = (yfield(xyinitial[0],xyinitial[1],tp1,streaktf),yfield(xyinitial[0],xyinitial[1],tp2,streaktf),yfield(xyinitial[0],xyinitial[1],tp3,streaktf),yfield(xyinitial[0],xyinitial[1],tp4,streaktf))

#ax.plot(xyinitial[0], xyinitial[1], color='black', linestyle='dashed', marker='o',markerfacecolor='black', markersize=14)


x_s = []
y_s = []

p = np.linspace(0,2,10)# now we want mulitple particles

for particle in p:
        xs = xyinitial[0]*np.exp(streaktf-particle)
        ys = xyinitial[1]*np.exp((-1/2)*(streaktf**2-particle**2))
        x_s.append(xs)
        y_s.append(ys)
        
        
#ax.plot(xs1, ys1, color='black', linestyle='dashed', marker='o',markerfacecolor='black', markersize=14)#4 point streakline
#ax.plot(x_s,y_s,linewidth = 4, color = 'm',linestyle='dashed')#actual streakline



#################################################################################################################################################################################################################
def path(t,xyp0):
    x = xyp0[0]
    y = xyp0[1]
    dypdt = x
    
    dxpdt = -y*t
    return dypdt,dxpdt

st = 0
xyp0 = [1,8]
tspan_p=[st,2]
t_eval_p = np.linspace(st,2,200)


sol_p = solve_ivp(path, tspan_p, xyp0, t_eval = t_eval_p)

tp = sol_p.t
xp = sol_p.y[0,:]
yp= sol_p.y[1,:]

ax.plot(xp,yp, linewidth =6)



#first path


xdata = []
ydata = []
line, = ax.plot(xdata, ydata,label = ('x0=1,y0=8,$t0$ = '+ str(tp1)))

def init_path():
    global line
    line, = ax.plot(xdata, ydata, linewidth = 6, color = 'b')
   
    return  line,
def update_path(time,ax,fig):
    
	xdata.append(xfield(firstpath[0],firstpath[1],firstpath[2],time))
	ydata.append(yfield(firstpath[0],firstpath[1],firstpath[2],time))
	line.set_data(xdata, ydata)

	return line,


#second path line


xdata1 = []
ydata1 = []
line1, = ax.plot(xdata1, ydata1,label = ('x0=1,y0=8,$t0$ = '+ str(tp2)))

def init_path1():
    global line1
    line1, = ax.plot(xdata1, ydata1,linewidth = 6, color = 'g')
    return  line1,
def update_path1(time,ax,fig):
    
	xdata1.append(xfield(secondpath[0],secondpath[1],secondpath[2],time))
	ydata1.append(yfield(secondpath[0],secondpath[1],secondpath[2],time))
	line1.set_data(xdata1, ydata1)
	return line1,


#third path line

xdata2 = []
ydata2 = []
line2, = ax.plot(xdata2, ydata2,label = ('x0=1,y0=8,$t0$ = '+ str(tp3)))

def init_path2():
    global line2
    line2, = ax.plot(xdata2, ydata2,linewidth = 6, color = 'r')
    ax.set_label("x0=1,y0=8,t0=0")
    return  line2,
def update_path2(time,ax,fig):
    
	xdata2.append(xfield(thirdpath[0],thirdpath[1],thirdpath[2],time))
	ydata2.append(yfield(thirdpath[0],thirdpath[1],thirdpath[2],time))
	line2.set_data(xdata2, ydata2)
    
	return line2,


xdata3 = []
ydata3 = []
line3, = ax.plot(xdata3, ydata3,label = ('x0=1,y0=8,$t0$ = '+ str(tp4)))

def init_path3():
    global line3
    line3, = ax.plot(xdata3, ydata3,linewidth = 6, color = 'y')
    return  line3,
def update_path3(time,ax,fig):
    
	xdata3.append(xfield(fourthpath[0],fourthpath[1],fourthpath[2],time))
	ydata3.append(yfield(fourthpath[0],fourthpath[1],fourthpath[2],time))
	line3.set_data(xdata3, ydata3)
	return line3,
#################################################################################################################################################################################
#moving dye
dyex = []
dyey = []


tt = np.linspace(Initial_Time,6, 20)
line4, = ax.plot(dyex, dyey, 'o')

def dye(t):
    x = 1+t
    y = 8
    dyex.append(x)
    dyey.append(y)
    line4.set_data(dyex, dyey)
    return line4,


#ani = FuncAnimation(fig, dye, frames=10, interval=200)



####################################3

quiv = animation.FuncAnimation(fig, update_quiver, frames = timespan_q,init_func=init_quiver,interval=intervals,fargs=(ax, fig),repeat =False)

path = animation.FuncAnimation(fig, update_path,frames=t, init_func=init_path, interval = intervals,fargs=(ax, fig),repeat = False)

#path2 = animation.FuncAnimation(fig, update_path1,frames=t, init_func=init_path1, interval = intervals,fargs=(ax, fig),repeat = False)

#path3 = animation.FuncAnimation(fig, update_path2,frames=t, init_func=init_path2, interval = intervals,fargs=(ax, fig),repeat = False)

#path4 = animation.FuncAnimation(fig, update_path3,frames=t, init_func=init_path3, interval = intervals,fargs=(ax, fig),repeat = False)

dye = animation.FuncAnimation(fig, dye, frames=t, interval=intervals)
'''
inital point
'''
ax.plot(xyinitial[0], xyinitial[1], color='black', linestyle='dashed', marker='o',markerfacecolor='black', markersize=14)
'''
final streak points
'''





#ax.plot(xs1, ys1, color='black', linestyle='dashed', marker='o',markerfacecolor='black', markersize=14)#4 point streakline
'''
entire streakline
'''
ax.plot(x_s,y_s,linewidth = 4, color = 'm',linestyle='dashed')#actual streakline



plt.xlim(0,Xaxis)
plt.ylim(0,Yaxis)
plt.legend(loc = "upper right", prop={'size': 10})
plt.axis('equal')
plt.show()


