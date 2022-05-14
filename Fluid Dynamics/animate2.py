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
streaktf = Final_Time

#axis format
Xaxis = 10
Yaxis = 10
NumVectors = 20


intervals  = 100 #how quickly in ms the plots update

#other initials

x = np.linspace(0,Xaxis, NumVectors)
y = np.linspace(0,Yaxis, NumVectors)
X,Y = np.meshgrid(x,y)

t = np.linspace(Initial_Time,Final_Time, 200)
print(len(t))
timespan_q = range(0,len(t))
print(len(timespan_q))















#streamplot

###################################################################################################################################################################################################################################


fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)


xx = np.linspace(0,Xaxis, NumVectors)
yy = np.linspace(0,Yaxis, NumVectors)
XX,YY = np.meshgrid(xx,yy)

stream_time_instant1 = 0.50
stream_time_instant2 = 1
stream_time_instant3 = 1.5
stream_time_instant4 = 2


UU = XX
VV1 = -YY*stream_time_instant1
VV2 = -YY*stream_time_instant2
VV3 = -YY*stream_time_instant3
VV4 = -YY*stream_time_instant4

#speed = np.sqrt(UU**2 + VV**2)



ax1.streamplot(XX, YY, UU, VV1, density = 1)
ax1.set_title('$t$ = '+ str(stream_time_instant1)+"s")
ax2.streamplot(XX, YY, UU, VV2, density = 1)
ax2.set_title('$t$ = '+ str(stream_time_instant2)+"s")
ax3.streamplot(XX, YY, UU, VV3, density = 1)
ax3.set_title('$t$ = '+ str(stream_time_instant3)+"s")
ax4.streamplot(XX, YY, UU, VV4, density = 1)
ax4.set_title('$t$ = '+ str(stream_time_instant4)+"s")

for ax in fig1.get_axes():
    ax.label_outer()









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
    ax.set_title('$t$ = '+ str(t[j]))
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
ax.set_title('$t$ = '+ str(t[0]))
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


#############################################################################3######################################################################################################################################

    #streaklines
#streak
sx = []
sy = []
def streak(t,xys):
    xss = xys[0]
    yss = xys[1]


    dysdt=xss

    dxsdt= -yss*t
    return dysdt,dxsdt

xys = [1,8]
teval = np.linspace(1,2,200)
tspan_s = [1,2]



sol_s = solve_ivp(streak, tspan_s, xys,t_eval = teval)
tp = sol_s.t
xss = sol_s.y[0,:]
yss= sol_s.y[1,:]
sx.append(xss)
sy.append(yss)

print(sx)
print(sy)

ax.plot(xss,yss)

firstpath = [1,8,0]
secondpath = [1,8,0.33]
thirdpath= [1,8,.66]
fourthpath = [1,8,1]


xyinitial = [1,8]


xs1 = (xfield(1,8,0,streaktf),xfield(1,8,0.33,streaktf),xfield(1,8,0.66,streaktf),xfield(1,8,1,streaktf))

ys1 = (yfield(1,8,0,streaktf),yfield(1,8,0.33,streaktf),yfield(1,8,0.66,streaktf),yfield(1,8,1,streaktf))

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
        
        
ax.plot(xs1, ys1, color='black', linestyle='dashed', marker='o',
     markerfacecolor='black', markersize=14)
ax.plot(x_s,y_s,linewidth = 4, color = 'm',linestyle='dashed')



######################################################################################################################################

#pathlines

#pathline initals

'''
#path
firstpath = [1,8,0]
secondpath = [2,7,0]
thirdpath = [3,6,0]
fourthpath = [1,7,0]

'''





#first path

x0=firstpath[0]
y0=firstpath[1]
t0=firstpath[2]
xdata = []
ydata = []
line, = ax.plot(xdata, ydata)

def init_path():
    global line
    line, = ax.plot(xdata, ydata, linewidth = 6, color = 'b')
    return  line,
def update_path(time,ax,fig):
    
	xdata.append(xfield(x0,y0,t0,time))
	ydata.append(yfield(x0,y0,t0,time))
	line.set_data(xdata, ydata)

	return line,


#second path line

x01=secondpath[0]
y01=secondpath[1]
t01=secondpath[2]
xdata1 = []
ydata1 = []
line1, = ax.plot(xdata1, ydata1)

def init_path1():
    global line1
    line1, = ax.plot(xdata1, ydata1,linewidth = 6, color = 'g')
    return  line1,
def update_path1(time,ax,fig):
    
	xdata1.append(xfield(x01,y01,t01,time))
	ydata1.append(yfield(x01,y01,t01,time))
	line1.set_data(xdata1, ydata1)
	return line1,


#third path line
x02=thirdpath[0]
y02=thirdpath[1]
t02=thirdpath[2]
xdata2 = []
ydata2 = []
line2, = ax.plot(xdata2, ydata2)

def init_path2():
    global line2
    line2, = ax.plot(xdata2, ydata2,linewidth = 6, color = 'r')
    return  line2,
def update_path2(time,ax,fig):
    
	xdata2.append(xfield(x02,y02,t02,time))
	ydata2.append(yfield(x02,y02,t02,time))
	line2.set_data(xdata2, ydata2)
	return line2,

#fourth path line
x03=fourthpath[0]
y03=fourthpath[1]
t03=fourthpath[2]
xdata3 = []
ydata3 = []
line3, = ax.plot(xdata3, ydata3)

def init_path3():
    global line3
    line3, = ax.plot(xdata3, ydata3,linewidth = 6, color = 'y')
    return  line3,
def update_path3(time,ax,fig):
    
	xdata3.append(xfield(x03,y03,t03,time))
	ydata3.append(yfield(x03,y03,t03,time))
	line3.set_data(xdata3, ydata3)
	return line3,
#################################################################################################################################################################################


quiv = animation.FuncAnimation(fig, update_quiver, frames = timespan_q,init_func=init_quiver,interval=intervals,fargs=(ax, fig),repeat =False)

path = animation.FuncAnimation(fig, update_path,frames=t, init_func=init_path, interval = intervals,fargs=(ax, fig),repeat = False)

path2 = animation.FuncAnimation(fig, update_path1,frames=t, init_func=init_path1, interval = intervals,fargs=(ax, fig),repeat = False)

path3 = animation.FuncAnimation(fig, update_path2,frames=t, init_func=init_path2, interval = intervals,fargs=(ax, fig),repeat = False)

path4 = animation.FuncAnimation(fig, update_path3,frames=t, init_func=init_path3, interval = intervals,fargs=(ax, fig),repeat = False)


plt.show()


