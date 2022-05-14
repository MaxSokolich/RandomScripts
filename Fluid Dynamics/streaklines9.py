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

#streamplot intials


#Quiver Initals
Initial_Time = 0
Final_Time = 2


xyinitial = [1,8]

intervals  = 100 #how quickly in ms the plots update

#streak








#Initials

streaktf = Final_Time

#axis format
Xaxis = 10
Yaxis = 10
NumVectors = 30




#other initials

x = np.linspace(0,Xaxis, NumVectors)
y = np.linspace(0,Yaxis, NumVectors)
X,Y = np.meshgrid(x,y)

t = np.linspace(Initial_Time,Final_Time, 200)

timespan_q = range(0,len(t))

#quiver
#################################################################################################################################################################################################################



def ufield(x,y,t):
    return x

def vfield(x,y,t):
    return -y*t



def update_quiver(j, ax, fig):
    u = ufield(X,Y,t[j])
    v = vfield(X,Y,t[j])
    Q.set_UVC(u, v)
    ax.set_title('$t$ = '+ str(round(t[j],3)),fontsize = 26)
    
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







firstpath = [xyinitial[0],xyinitial[1],0]
secondpath = [xyinitial[0],xyinitial[1],0.33]
thirdpath= [xyinitial[0],xyinitial[1],0.66]
fourthpath = [xyinitial[0],xyinitial[1],1]

xs1 = (xfield(xyinitial[0],xyinitial[1],0,streaktf),xfield(xyinitial[0],xyinitial[1],0.33,streaktf),xfield(xyinitial[0],xyinitial[1],0.66,streaktf),xfield(xyinitial[0],xyinitial[1],1,streaktf))

ys1 = (yfield(xyinitial[0],xyinitial[1],0,streaktf),yfield(xyinitial[0],xyinitial[1],0.33,streaktf),yfield(xyinitial[0],xyinitial[1],0.66,streaktf),yfield(xyinitial[0],xyinitial[1],1,streaktf))

ax.plot(xyinitial[0], xyinitial[1], color='black', linestyle='dashed', marker='o',
     markerfacecolor='black', markersize=14)


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



#first path


xdata = []
ydata = []
line, = ax.plot(xdata, ydata,label = ("x0=1,y0=8,t0=0"))

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
line1, = ax.plot(xdata1, ydata1,label = ("x0=1,y0=8,t0=0.333"))

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
line2, = ax.plot(xdata2, ydata2,label = ("x0=1,y0=8,t0=0.666"))

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
line3, = ax.plot(xdata3, ydata3,label = ("x0=1,y0=7,t0=1"))

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




####################################3

quiv = animation.FuncAnimation(fig, update_quiver, frames = timespan_q,init_func=init_quiver,interval=intervals,fargs=(ax, fig),repeat =False)

path = animation.FuncAnimation(fig, update_path,frames=t, init_func=init_path, interval = intervals,fargs=(ax, fig),repeat = False)

#path2 = animation.FuncAnimation(fig, update_path1,frames=t, init_func=init_path1, interval = intervals,fargs=(ax, fig),repeat = False)

#path3 = animation.FuncAnimation(fig, update_path2,frames=t, init_func=init_path2, interval = intervals,fargs=(ax, fig),repeat = False)

#path4 = animation.FuncAnimation(fig, update_path3,frames=t, init_func=init_path3, interval = intervals,fargs=(ax, fig),repeat = False)


#ax.plot(xs1, ys1, color='black', linestyle='dashed', marker='o',markerfacecolor='black', markersize=14)#4 point streakline

#ax.plot(x_s,y_s,linewidth = 4, color = 'm',linestyle='dashed')#actual streakline


plt.legend(loc = "upper right", prop={'size': 22})
plt.axis('equal')
plt.show()


