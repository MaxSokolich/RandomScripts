#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 10:28:41 2022

@author: bizzarohd
"""
#https://machinelearningmastery.com/a-gentle-introduction-to-particle-swarm-optimization/

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#define obective function
def function(x,y):
    f = np.sin(x) + np.sin(y)
    return f

#create coordinates
x = np.linspace(0,5,100)
y = np.linspace(0,5,100)
X,Y = np.array(np.meshgrid(x,y))
Z = function(X,Y)

#caclualtes the x and y coords where Z is at a minimum
flattenX = X.ravel()
flattenY = Y.ravel()

xmin = flattenX[Z.argmin()] #argmin returns the index with the minimum value, #min just prints the minimum value
ymin = flattenY[Z.argmin()]


#intitilaize particles
iterations= 5
n_particles = 20
np.random.seed(10)
Xp = np.random.rand(2, n_particles) * 5   #vector position of particle
Vp = np.random.randn(2, n_particles)*0.2    #vector velocity of particle
print(Xp)
print(Vp, "\n")








######################################################################################################
'''
intilize the particles best known position to its intitial position 

'''
pbest = Xp

'''
for each iteration, compute each particles solution value
vector: function output
'''
pbest_obj = function(Xp[0], Xp[1])  #initlilize the particles objective cost function (function values to minimize for each particle)

'''
update the global best as the particles position that yieled the lowest function value usign argmin
vector: particle position output
'''
gbest = pbest[:, pbest_obj.argmin()]  

'''
update the global objective as the minimum function value found from gbest
 - scaler: function output
'''
gbest_obj = pbest_obj.min()


print(pbest)

print(gbest, "\n")
print(gbest_obj)



##############################
                             #
                             #
                             #
#        ONE ITERATION       #
                             #
                             #
                             #
##############################                             

def update_the_particles_positions_velocities():
    global Vp, Xp, pbest, pbest_obj, gbest, gbest_obj
    
    '''
    update the particles velocity by subtracting the global best at the time by the previous particle position to 
    force the vector direction of all the particles towards the global minimum
    
    
    its equal to the current velcoity + 2 terms
    
    term 1: subtract the best particle positions found by the current particle poisitions
    
    term 2: subtracting the global best at the time by the previous particle position to 
    force the vector direction of all the particles towards the global minimum
    '''
    c1 = 0.1
    c2 = 0.1
    w = 0.8
    r = np.random.rand(2)
    Vp = w * Vp + c1 * r[0] * (pbest - Xp) + c2 * r[1] * (gbest.reshape(-1,1) - Xp) 
    
    
    
    '''
    now update particles position based on calcualted velocity
    '''
    Xp = Xp + Vp
   
    
    
    '''
    define a general objective function
    '''
    obj = function(Xp[0], Xp[1])
    
    
    
    '''
    set the best position of the each particle as the previous position of each particle. 
    
    this is sort of the if statement:
        
        if a particles present position is better than its previsou best position, update it
        
        i.e. loop through pbest, and equat
    '''
    
   
    pbest[:, (pbest_obj >= obj)]   =    Xp[:, (pbest_obj >= obj)]
    
    pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
    
    
    '''
    now find the best particle from this iteration and update the global best with this NEW best particle.
    '''
    
    gbest = pbest[:, pbest_obj.argmin()]
    
    gbest_obj = pbest_obj.min()
    
    
    
    
    print(Vp, "\n")
    print(pbest_obj)
    
   
    
    print("\n\n\n\n")



#PLOT everything

fig, ax = plt.subplots(figsize = (13,10))
fig.set_tight_layout(True)

img = ax.imshow(Z, extent = [0,5,0,5], cmap = 'viridis', alpha = 0.7)
fig.colorbar(img, ax=ax)


ax.plot([xmin], [ymin], marker = '*', color = 'k')

contour = ax.contour(X,Y,Z, 11, alpha = 0.7)

particles = ax.scatter(Xp[0], Xp[1], color = 'k', alpha = 1,s = 100)
velocities = ax.quiver(Xp[0], Xp[1], Vp[0], Vp[1], width = 0.005, angles='xy', scale_units = 'xy', scale = .5)
pbest_plot = ax.scatter(pbest[0], pbest[1], marker = 'o')
gbest_plot = ax.scatter(gbest[0],gbest[1], color = 'g', alpha = 1,s = 50)


#display animation
def animate(i):
    title = 'Iteration {:02d}'.format(i)
    update_the_particles_positions_velocities()
    
    ax.set_title(title)
    
    #update the plot variables with the newly calcualted pbest, Xp, velcoties etc by using set_offsets
    pbest_plot.set_offsets(pbest.T)
    particles.set_offsets(Xp.T)
    velocities.set_offsets(Xp.T)
    velocities.set_UVC(Vp[0],Vp[1])
    gbest_plot.set_offsets(gbest.reshape(1,-1))
    return ax, pbest_plot, particles, velocities, gbest_plot

tspan = list(range(iterations))
anim = FuncAnimation(fig, animate, frames = tspan, interval = 1000, blit = False)
    
    
print("\n\n\n\n")
print("PSO found best solution at f({})={}".format(gbest, gbest_obj))
print("Global optimal at f({})={}".format([xmin,ymin], function(xmin,ymin)))

    










