#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 21 15:44:56 2022

@author: bizzarohd
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 12:41:23 2022

@author: bizzarohd
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation




#Step 1: Problem Definition
#%%
'''
define optimization problem which is being solved by PSO
'''
#Define Cost Function
def CostFunction(X):
    Z = (X[0]-3.14)**2 + (X[1]-2.72)**2 + np.sin(3*X[0]+1.41) + np.sin(4*X[1]-1.73)
    #Z = np.sin(X[0]) + np.cos(X[1])
    return Z



nVar = 2                         # the number of desicion or unknown variables (what is the dimension of our search space)
VarSize = np.zeros([nVar])       # any solution of our seach space is size 1 row and nvar columuns. so our solution are horizontal vecots
VarMin = -7                       # lower bound of desicison variables, our 5 desicion variables are real numbers from -10 to 10
VarMax = 15                      # upper bound of desision variables

                                    # we are search for a value in this range that minimizes our cost function

#%%



#Step 2:  Parameters of PSO
#%%

MaxIt = 50                        # how many times the PSO will iterate for

nPop = 20                     # population size or swarm size or number of particles in the swarm

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
    """Class for storing Particle varaibles , AKA
    (Poistion= [x,y], velocity = [x,y], cost = C, Personal_Best_Pos = [x,y] , Personal_Best_Cost = C)

    """

    def __init__(self):
        self.Position = 0
        self.Velocity = 0
        self.Cost = 0
        self.Personal_Best_Pos = 0
        self.Personal_Best_Cost = 0
    
    def set_position(self, Position):
        self.Position = Position

    def set_velocity(self, Velocity):
        self.Velocity = Velocity

    def set_cost(self, Cost):
        self.Cost = Cost
        
    def set_Personal_Best_Pos(self, Personal_Best_Pos):
        self.Personal_Best_Pos = Personal_Best_Pos
        
    def set_Personal_Best_Cost(self, Personal_Best_Cost):
        self.Personal_Best_Cost = Personal_Best_Cost
          
        
#create population array



#Initilize Global Best (initlizlly it holds the worst value)
GlobalBestCost = 100000
GlobalBestPosition = 0







# loop through empty particle template and intilize/ define the initial positions etc
Particle_Array = []
for i in range(nPop):
    Particle = Empty_Particle()
    
    Particle.set_position(np.random.uniform(VarMin, VarMax, nVar))
    Particle.set_velocity(np.random.uniform(VarMin, VarMax, nVar)*.1)
    Particle.set_cost(CostFunction(Particle.Position))
    Particle.set_Personal_Best_Pos(Particle.Position)
    Particle.set_Personal_Best_Cost(Particle.Cost)
    
    Particle_Array.append(Particle)
    print(Particle.Velocity)
    #update personal and global bests based on these preliinary values
    
    if Particle.Personal_Best_Cost < GlobalBestCost:
        GlobalBestCost = Particle.Personal_Best_Cost
        GlobalBestPosition = Particle.Personal_Best_Pos
    


#%%



#Step 4: Iteration: Main Loop of PSO
#%%


BestCosts = []

Total_Pos_List = []
Total_Vel_List = []


for it in range(MaxIt):
    BestCosts.append(GlobalBestCost)
    print("Iterarton"+str(it))
    print("      Global Best Cost = ", GlobalBestCost)
    print("      Global Best Position = ", GlobalBestPosition)
    
    #Record positions from each generation and append to lsit
    Pos_Generation_List = []
    Total_Pos_List.append(Pos_Generation_List)
    
    #record velcoitys
    Vel_Generation_List = []
    Total_Vel_List.append(Vel_Generation_List)
   
   

    for i in range(len(Particle_Array)):
        
        #Update Velocity
        r = np.random.rand(2)
        Particle_Array[i].Velocity = w * Particle_Array[i].Velocity + (r[0] * c1 * (Particle_Array[i].Personal_Best_Pos - Particle_Array[i].Position)) + (r[1] * c2 * (GlobalBestPosition - Particle_Array[i].Position))
        #Now move each particle based on new velocity
        Particle_Array[i].Position = Particle_Array[i].Position + Particle_Array[i].Velocity
        
        #Record individual positions
        Pos_Generation_List.append(Particle_Array[i].Position)
    
        #Record individual velociuues
        Vel_Generation_List.append(Particle_Array[i].Velocity)
    
       
        #Update Cost
        Particle_Array[i].Cost = CostFunction(Particle_Array[i].Position)
        if Particle_Array[i].Cost < Particle_Array[i].Personal_Best_Cost:
            Particle_Array[i].Personal_Best_Pos = Particle_Array[i].Position
            Particle_Array[i].Personal_Best_Cost = Particle_Array[i].Cost
            if Particle_Array[i].Personal_Best_Cost < GlobalBestCost:
                GlobalBestCost = Particle_Array[i].Personal_Best_Cost
                GlobalBestPosition = Particle_Array[i].Position
       
        

Total_Pos_List = np.array(Total_Pos_List)
Total_Vel_List = np.array(Total_Vel_List)


#Step 5: Animate if 2D
#%%


#print(BestCosts)
fig, ax = plt.subplots(figsize=(13,8))
ax.set_xlim([VarMin,VarMax])
ax.set_ylim([VarMin,VarMax])


Pos_Plot = ax.scatter(Total_Pos_List[0,:,0],Total_Pos_List[0,:,1])
Arrow_Plot = ax.quiver(Total_Pos_List[0,:,0],Total_Pos_List[0,:,1],Total_Vel_List[0,:,0],Total_Vel_List[0,:,1], width=0.005, angles='xy', scale_units='xy', scale=1)


#Create contours
x, y = np.array(np.meshgrid(np.linspace(VarMin,VarMax,200), np.linspace(VarMin,VarMax,200)))
Z = CostFunction([x,y])
Countor_Plot = ax.contour(x, y, Z, 10)
Color_Plot = ax.imshow(Z, extent = [VarMin,VarMax,VarMin,VarMax])




def animate(i):
    title = 'Iteration {:02d}'.format(i)
    ax.set_title(title)
    data= np.array([Total_Pos_List[i,:,0],Total_Pos_List[i,:,1]])
    Pos_Plot.set_offsets(data.T)
    Arrow_Plot.set_offsets(data.T)
    Arrow_Plot.set_UVC(Total_Vel_List[i,:,0], Total_Vel_List[i,:,1])
    return ax,  Pos_Plot, Arrow_Plot
   

#plt.figure()
#plt.plot(np.arange(0,MaxIt), BestCosts)


ani = animation.FuncAnimation(fig, animate, frames=list(range(1,MaxIt)), interval=500, repeat = False)
#Step 6: Results
#%%







#%%
