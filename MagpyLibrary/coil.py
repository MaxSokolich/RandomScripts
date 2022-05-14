#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 17:02:04 2021

@author: bizzaro
"""
'''
https://magpylib.readthedocs.io/en/gettingstartedreview/_pages/2_guideExamples/
#https://magpylib.readthedocs.io/_/downloads/en/latest/pdf/


for any coil configureation with n number of loops 
measure the magnetic field at any position

Magpylib uses units of
• [mT]: for the B-field and the magnetization (mu0*M). • [kA/m]: for the H-field.
• [mm]: for all position inputs.
• [deg]: for angle inputs by default.
• [A]: for current inputs.

'''
#current in amps


import numpy as np
import magpylib as mag3
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R



fig = plt.figure(figsize=(10,10))
ax2 = plt.axes(projection='3d')

fig1, ax1 = plt.subplots()
fig2, ax3 = plt.subplots()


perm = (1.26*(10**(-4)))
perm0 = (1.256*(10**(-6)))
num_loops_D = 7
num_loops_L = 30
space = 120
L = .04
EM_diamter = 5 #mm
EM_length = .04*1000  #mm
measurement_location = [15,0,0]




###############################################
N = num_loops_D*num_loops_L

coil1_current = 1
coil2_current = 1
coil3_current = 0
coil4_current = 0
'''
magnitization1 = ((perm/perm0)-1)*((N*coil1_current)/L)/1000    #M = n*coil1_current
magnitization2 = ((perm/perm0)-1)*((N*coil2_current)/L)/1000     #((1/perm0)-(1/perm))*B
magnitization3 = ((perm/perm0)-1)*((N*coil3_current)/L)/1000
magnitization4 = ((perm/perm0)-1)*((N*coil4_current)/L)/1000
'''


#%%
#Create coils and assign a collection



coil1 = [[mag3.current.Circular(current=coil1_current, diameter=h,position = (20,0,z)) for z in np.linspace( 0,L*1000,num_loops_L)] for h in np.linspace(5.4,20,num_loops_D)]
coil2 = [[mag3.current.Circular(current=-coil2_current, diameter=h,position = (-20,0,z)) for z in np.linspace( 0,L*1000,num_loops_L)] for h in np.linspace(5.4,20,num_loops_D)]
coil3 = [[mag3.current.Circular(current=coil3_current, diameter=h,position = (0,20,z)) for z in np.linspace( 0,L*1000,num_loops_L)] for h in np.linspace(5.4,20,num_loops_D)]
coil4 = [[mag3.current.Circular(current=-coil4_current, diameter=h,position = (0,-20,z)) for z in np.linspace( 0,L*1000,num_loops_L)] for h in np.linspace(5.4,20,num_loops_D)]




c1 = mag3.Collection(coil1)
c2 = mag3.Collection(coil2)
c3 = mag3.Collection(coil3)
c4 = mag3.Collection(coil4)

R1 = R.from_euler('y', 90, degrees=True) 
R2 = R.from_euler('y', -90, degrees=True) 
R3 = R.from_euler('x', -90, degrees=True) 
R4 = R.from_euler('x', 90, degrees=True) 

c1.rotate(R1 ,anchor = [20,0,0])
c2.rotate(R2 ,anchor = [-20,0,0])
c3.rotate(R3 ,anchor = [0,20,0])
c4.rotate(R4 ,anchor = [0,-20,0])

coils = mag3.Collection(c1,c2,c3,c4)
#%%   

#%%
#create cores and assign collection
mag1_strength = (0,0,(70*c1.getB(40,0,0)[0]))
mag2_strength = (0,0,(70*c1.getB(-40,0,0)[0]))
mag3_strength = (0,0,(70*c1.getB(0,40,0)[0]))
mag4_strength = (0,0,(70*c1.getB(-0,-40,0)[0]))


EM1_position = (40,0,0)
EM2_position = (-40,0,0)
EM3_position = (0,40,0)
EM4_position = (0,-40,0)

EM1_orient = R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True)
EM2_orient = R.from_rotvec(-90 * np.array([0, 1, 0]), degrees=True)
EM3_orient = R.from_rotvec(-90 * np.array([1, 0, 0]), degrees=True)
EM4_orient = R.from_rotvec(90 * np.array([1, 0, 0]), degrees=True)

r1 = mag3.magnet.Cylinder(magnetization=mag1_strength , dimension=(EM_diamter,EM_length), position = EM1_position, orientation=EM1_orient)
r2 = mag3.magnet.Cylinder(magnetization=mag2_strength, dimension=(EM_diamter,EM_length), position = EM2_position, orientation=EM2_orient)
r3 = mag3.magnet.Cylinder(magnetization=mag3_strength , dimension=(EM_diamter,EM_length), position = EM3_position, orientation=EM3_orient)
r4 = mag3.magnet.Cylinder(magnetization=mag4_strength, dimension=(EM_diamter,EM_length), position = EM4_position, orientation=EM4_orient)

rods = mag3.Collection(r1,r2,r3,r4)
#%%

col = mag3.Collection(coils,rods)
mag3.display(col, axis=ax2)


#%%    
#display field in xz-plane macro    




xs = np.linspace(-space/2,space/2,40)
ys = np.linspace(-space/2,space/2,40)
X,Y = np.meshgrid(xs,ys)

B = np.array([[mag3.getB(col,[x,y,0],sumup=False) for x in xs] for y in ys])

#contour
Bamp = np.linalg.norm(B,axis=2)
cont = ax1.contourf(X,Y,Bamp,50,cmap='rainbow')
fig1.colorbar(cont, ax=ax1)

#streamplot
U = B[:,:,0]
V = B[:,:,1]
W = B[:,:,2]

res = ax1.streamplot(X, Y, U, V, color=np.sqrt(U**2+V**2),density = 1)
ax1.set_title("100mm by 100mm ROI Magnetic Field Lines. Map in mT")
ax1.set_xlabel("x (mm)")
ax1.set_ylabel("y (mm)")



#%%

#%%
#Contour mapping
'''
#Bamp = np.linalg.norm(B,axis=2)

#cont = ax1.contourf(X,Y,Bamp,100,cmap='rainbow')
#fig1.colorbar(cont)
'''
#%%


#%%
#display streamplot on 3D display
lines1 = res.lines.get_paths()


for line in lines1:
    old_x = line.vertices.T[0]
    old_y = line.vertices.T[1]
    # apply for 2d to 3d transformation here
    new_z = np.exp(-(old_x ** 2 + old_y ** 2) / 4)
    new_x = 1 * old_x
    new_y = 1 * old_y
    ax2.plot(new_x, new_y, new_z, 'b')
    

#%%

#%%

#display field in xz-plane micro

space_micro = 1 #mm
xm = np.linspace(-space_micro/2,space_micro/2,20)
ym = np.linspace(-space_micro/2,space_micro/2,20)
Xm,Ym = np.meshgrid(xm,ym)

Bm = np.array([[col.getB([x,y,0]) for x in xm] for y in ym])

#contour plot
Bampm = np.linalg.norm(Bm,axis=2)
contm = ax3.contourf(Xm,Ym,Bampm,50,cmap='rainbow')
fig2.colorbar(contm, ax=ax3)


#streamplot
Um = Bm[:,:,0]
Vm = Bm[:,:,1]
Wm = Bm[:,:,2]

resm = ax3.streamplot(Xm, Ym, Um, Vm, color=np.sqrt(Um**2+Vm**2),density = 1)
ax3.set_title("1mm by 1mm ROI Magnetic Field Lines. Map in mT")
ax3.set_xlabel("x (mm)")
ax3.set_ylabel("y (mm)")



#%%
#print indivudual field strength at position
print(col.getB(measurement_location))
ax1.plot(measurement_location[0], measurement_location[1], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=10)
ax2.plot(measurement_location[0], measurement_location[1], measurement_location[2], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=5)
#ax3.plot(measurement_location[0], measurement_location[1], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=10)

#%%
