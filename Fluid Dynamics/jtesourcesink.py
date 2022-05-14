#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 09:58:46 2021

@author: bizzaro
"""

# ELEMENTARY FLOW - SOURCE/SINK FLOW
# Written by: JoshTheEngineer
# YouTube   : www.youtube.com/joshtheengineer
# Website   : www.joshtheengineer.com
# Started: 02/19/19
# Updated: 02/19/19 - Transferred from MATLAB to Python
#                   - Works as expected

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# %% KNOWNS

lmbda = 1                                                                       # Source/sink strength (+: Source, -: Sink)
X0    = 0                                                                       # Source/sink X coordinate
Y0    = 0    
V = 1
alpha = 0                                                                   # Source/sink Y coordinate

# %% CALCULATIONS

# Create grid
numX   = 100                                                                    # Number of X points
numY   = 100                                                                    # Number of Y points
X      = np.linspace(-10,10,numX)                                               # X-point array
Y      = np.linspace(-10,10,numY)                                               # Y-point array
XX, YY = np.meshgrid(X,Y)                                                       # Create the meshgrid

# Solve for velocities
Vx = np.zeros([numX,numY])                                                      # Initialize X velocity component
Vy = np.zeros([numX,numY])                                                      # Initialize Y velocity component
                                                     # Initialize velocity magnitude
Vr = np.zeros([numX,numY])                                                      # Initialize radial velocity component
r  = np.zeros([numX,numY])                                                      # Initialize radius
for i in range(numX):                                                           # Loop over X points
    for j in range(numY):                                                       # Loop over Y points
        x       = XX[i,j]                                                       # X coordinate
        y       = YY[i,j]                                                       # Y coordinate
                                                                                # Y distance from source/sink
                                                                                # Distance from source/sink
        Vx[i,j] = (V *np.cos(alpha*(np.pi/180)))  +  (lmbda*(x - X0))/(2*np.pi*((x - X0)**2 + (y - Y0)**2))                                     # Compute X velocity component
        Vy[i,j] = (V *np.sin(alpha*(np.pi/180)))  +  (lmbda*(y - Y0))/(2*np.pi*((x - X0)**2 + (y - Y0)**2))                                   # Compute Y velocity component
                                  # Compute velocity
                                                                                 # Compute radial velocity component

#uq = (V *np.cos(alpha*(np.pi/100)))+(-circulation *(xq-x0))/(2*np.pi*(((xq-x0)**2)+((yq-y0)**2)))
#vq = (V *np.sin(alpha*(np.pi/100)))+(circulation *(yq-y0))/(2*np.pi*(((xq-x0)**2)+((yq-y0)**2)))

# %% COMPUTE CIRCULATIONS
def COMPUTE_CIRCULATION(a,b,x0,y0,numT,Vx,Vy,X,Y):
    
    t     = np.linspace(0,2*np.pi,numT)                                         # Discretized ellipse into angles [rad]
    xC    = a*np.cos(t) + x0                                                    # X coordinates of ellipse
    yC    = b*np.sin(t) + y0                                                    # Y coordinates of ellipse
    fx    = interpolate.RectBivariateSpline(Y,X,Vx)                             # Interpolate X velocities from grid to ellipse points
    fy    = interpolate.RectBivariateSpline(Y,X,Vy)                             # Interpolate Y velocities from grid to ellipse points
    VxC   = fx.ev(yC,xC)                                                        # X velocity component on ellipse
    VyC   = fy.ev(yC,xC)                                                        # Y velocity component on ellipse
    Gamma = -(np.trapz(VxC,xC) + np.trapz(VyC,yC))                              # Compute integral using trapezoid rule
    
    return Gamma, xC, yC, VxC, VyC

a    = 1.5                                                                      # Horizontal axis half-length
b    = 1.5                                                                      # Vertical axis half-length
x0   = 0                                                                        # Ellipse center X coordinate
y0   = 0                                                                        # Ellipse center Y coordinate
numT = 100                                                                      # Number of points along ellipse
Gamma, xC, yC, VxC, VyC = COMPUTE_CIRCULATION(a,b,x0,y0,numT,Vx,Vy,X,Y)         # Call circulation calculation
print("Circulation: ", Gamma)                                                   # Display circulation result

# %% PLOTTING

# Plot quiver
fig = plt.figure(1)                                                             # Create figure
plt.cla()                                                                       # Get ready for plotting
plt.quiver(X,Y,Vx,Vy)
print(Vx)     
plt.streamplot(X,Y,Vx,Vy)      
                                                  # Plot velocity vectors
plt.plot(xC,yC,'b-')                                                            # Plot ellipse
plt.title('Source/Sink Flow')                                                   # Set title
plt.xlabel('X-Axis')                                                            # Set X-label
plt.ylabel('Y-Axis')                                                            # Set Y-label
plt.xlim([-2, 2])                                                               # Set X-limits
plt.ylim([-2, 2])                                                               # Set Y-limits
plt.gca().set_aspect('equal')                                                   # Set axes equal
plt.show()                                                                      # Display plot
