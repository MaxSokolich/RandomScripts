#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:17:20 2021

@author: bizzaro
"""
# %%
import numpy as np
import matplotlib.pyplot as plt


# %%





# %%
fig = plt.figure()
ax = plt.subplot()

plt.xlim(-6, 6)
plt.ylim(-6, 6)

#initials

x0 = 0
y0 = 0






#stream
X = np.linspace(-10, 10, 50)
Y = np.linspace(-10,10, 50)
x,y = np.meshgrid(X, Y)

# %%
def u(alpha,V,y0,x0):
    uq = (V *np.cos(alpha*(np.pi/100))) + (-strength *(x-x0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2)))
    return uq
def v(alpha,V,y0,x0):
    vq = (V *np.sin(alpha*(np.pi/100)))+(strength *(y-y0))/(2*np.pi*(((x-x0)**2)+((y-y0)**2))) 
    return vq
#SOURCE SINK
# %%
strength  = 5 #m/s
numSL = 30  
V = 1
alpha = 0

#uq = (V *np.cos(alpha*(np.pi/100)))+(-strength *(xq-x0))/(2*np.pi*(((xq-x0)**2)+((yq-y0)**2)))
#vq = (V *np.sin(alpha*(np.pi/100)))+(strength *(yq-y0))/(2*np.pi*(((xq-x0)**2)+((yq-y0)**2)))                                                        
Xsl   = -10*np.ones(numSL)                                                      # Streamline starting X coordinates
Ysl   = np.linspace(-10,10,numSL)                                               # Streamline starting Y coordinates
XYsl  = np.vstack((Xsl.T,Ysl.T)).T 

speed = np.sqrt(u(alpha,V,y0,x0)*u(alpha,V,y0,x0) + v(alpha,V,y0,x0)*v(alpha,V,y0,x0))
plt.quiver(x,y,u(alpha,V,y0,x0),v(alpha,V,y0,x0))  
plt.streamplot(x,y,u(alpha,V,y0,x0),v(alpha,V,y0,x0), linewidth=speed,density = 10, color=u(alpha,V,y0,x0), arrowstyle='-',start_points=XYsl)
plt.xlim(-6, 6)
plt.ylim(-6, 6)
print(u(alpha,V,y0,x0))

plt.show()
# %%

#VORTEX
# %%
circulation  = 20 #m/s
numSL = 30   
V = 1
alpha = 0



    


