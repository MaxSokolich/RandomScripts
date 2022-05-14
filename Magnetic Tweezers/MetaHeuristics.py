#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 12:41:23 2022

@author: bizzarohd
"""

import numpy as np
import matplotlib.pyplot as plt
np.random.seed(10)





#Step 1: Problem Definition
#%%
'''
define optimization problem which is being solved by PSO
'''
#Define Cost Function
def CostFunction(X):
    def sphere(X):
        Z = sum(X**2)
        return Z
    return sphere(X)

nVar = 2                           # the number of desicion or unknown variables (what is the dimension of our search space)

VarSize = np.zeros([nVar])       # any solution of our seach space is size 1 row and nvar columuns. so our solution are horizontal vecots

VarMin = -10                        # lower bound of desicison variables, our 5 desicion variables are real numbers from -10 to 10
VarMax = 10                         # upper bound of desision variables

                                    # we are search for a value in this range that minimizes our cost function

#%%



#Step 2:  Parameters of PSO
#%%

MaxIt = 10                         # how many times the PSO will iterate for

nPop = 5                         # population size or swarm size or number of particles in the swarm

w = .8                               # interia Coefficent
c1 = 0.1                              # Personal or Acceleration Coeffient
c2 = 0.1                            # Social or Global Coefficent


#%%


#Step 3: Initilization
#%%
'''
evaluate the particles and intizlize the values of personal best and global best
'''

#the particle template
class Empty_Particle:

    def __init__(self, Position, Velocity, Cost, Personal_Best_Pos, Personal_Best_Cost):
        self.Position = Position
        self.Velocity = Velocity
        self.Cost = Cost
        self.Personal_Best_Pos = Personal_Best_Pos
        self.Personal_Best_Cost = Personal_Best_Cost
        
          
#create population array
p1 = Empty_Particle([], [], [], [], [])
p2 = Empty_Particle([], [], [], [], [])
p3 = Empty_Particle([], [], [], [], [])
p4 = Empty_Particle([], [], [], [], [])
p5 = Empty_Particle([], [], [], [], [])

Particles = [p1,p2,p3,p4,p5]


#Initilize Global Best (initlizlly it holds the worst value)
GlobalBestCost = 1000
BestCosts = np.zeros(MaxIt)

# loop through particles and intilize/ define the intilial positions etc
for i in Particles:
    
    i.Position = np.random.rand(2) * 5
    i.Velocity = np.random.rand(2) * .01
    
    
    #Evaluate Particle
    i.Cost = CostFunction(i.Position)
  
    #update the personal best for each particl
    i.Personal_Best_Pos = i.Position
    i.Personal_Best_Cost = i.Cost
    
    #particles = ax.scatter(i.Position[0], i.Position[1], color = 'k', alpha = 1,s = 100)
    #velocities = ax.quiver(i.Position[0], i.Position[1],  i.Velocity[0],  i.Velocity[1], width = 0.005, scale_units = 'xy', scale = .01)
    

    
    #Update Global Best (comapre personal best to global best)
    if i.Personal_Best_Cost < GlobalBestCost:
        GlobalBestCost = i.Personal_Best_Cost
    

#%%



#Step 4: Iteration: Main Loop of PSO
#%%




for it in range(MaxIt):
    for i in Particles:
     
        BestCosts[it] = GlobalBestCost
        Gobal_Best_Position = i.Position
        print(BestCosts[it])
        #new velocity value is:
        r = np.random.rand(2)
        
        i.Velocity = w * i.Velocity + r[0] * c1 *(i.Personal_Best_Cost - i.Position) + c2* r[1] * (Gobal_Best_Position - i.Position)
        i.Position = i.Position + i.Velocity
        
        i.Cost = CostFunction(i.Position)
        if i.Cost < i.Personal_Best_Cost:
            i.Personal_Best_Pos = i.Position
            i.Personal_Best_Cost = i.Cost
            if i.Personal_Best_Cost < GlobalBestCost:
                GlobalBestCost = i.Personal_Best_Cost
                Gobal_Best_Position = i.Position
            
        
        fig, ax = plt.subplots(figsize = (13,10))
        fig.set_tight_layout(True)

        ax.set_xlim([0,5])
        ax.set_ylim([0,5])
        particles = ax.scatter(i.Position[0], i.Position[1], color = 'k', alpha = 1,s = 100)
        
#store the best cost value at every iteration 
          
#%%



#Step 5: Results
#%%




#%%