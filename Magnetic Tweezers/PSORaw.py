#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:02:08 2022

@author: bizzarohd
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
def f(x,y):
    "Objective function"
    return np.sin(x) + np.sin(y)
    
# Compute and plot the function in 3D within [0,5]x[0,5]
x, y = np.array(np.meshgrid(np.linspace(0,5,100), np.linspace(0,5,100)))
z = f(x, y)
 
# Find the global minimum
x_min = x.ravel()[z.argmax()]
y_min = y.ravel()[z.argmax()]
 
# Hyper-parameter of the algorithm
c1 = .1
c2 = .1
w = .8
 
# Create particles
n_particles = 25
np.random.seed(10)
X = np.random.rand(2, n_particles) * 5
V = np.random.randn(2, n_particles) * 0.1
 
# Initialize data
personal_best = X
personal_best_obj = f(X[0], X[1])
gbest = personal_best[:, personal_best_obj.argmax()]
gbest_obj = personal_best_obj.max()

#print("X  =  ", X)
#print("personal_best  =  ", personal_best)
#print(gbest, gbest_obj,"\n\n")

def update():
    "Function to do one iteration of particle swarm optimization"
    global V, X, personal_best, personal_best_obj, gbest, gbest_obj, obj
    # Update params
    r1, r2 = np.random.rand(2)
    V = w * V + c1*r1*(personal_best - X) + c2*r2*(gbest.reshape(-1,1)-X)
    X = X + V
    obj = f(X[0], X[1])
    
    #if a particles position is better than its previous position ipdate it
    
   
    personal_best[:, (personal_best_obj <= obj)] = X[:, (personal_best_obj <= obj)]
    personal_best_obj = np.array([personal_best_obj, obj]).max(axis=0)
   
    gbest = personal_best[:, personal_best_obj.argmax()]
    gbest_obj = personal_best_obj.max()
    #print("X  =  ", X)
    #print("personal_best  =  ", personal_best)
    #print(gbest, gbest_obj,"\n\n")




for i in range(50):
    update()
    
    
    fig, ax = plt.subplots(figsize = (13,10))
    fig.set_tight_layout(True)

    img = ax.imshow(z, extent = [0,5,0,5], cmap = 'viridis', alpha = 0.7)
    fig.colorbar(img, ax=ax)


    ax.plot([x_min], [y_min], marker = '*', color = 'k')

    contour = ax.contour(x,y,z, 11, alpha = 0.7)

    particles = ax.scatter(X[0], X[1], color = 'k', alpha = 1,s = 100)
    velocities = ax.quiver(X[0], X[1], V[0], V[1], width = 0.005, angles='xy', scale_units = 'xy', scale = .5)
    personal_best_plot = ax.scatter(personal_best[0], personal_best[1], marker = 'o')
    gbest_plot = ax.scatter(gbest[0],gbest[1], color = 'g', alpha = 1,s = 50)


 
print("PSO found best solution at f({})={}".format(gbest, gbest_obj))
print("Global optimal at f({})={}".format([x_min,y_min], f(x_min,y_min)))