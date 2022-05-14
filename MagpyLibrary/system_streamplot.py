#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 14:45:02 2021

@author: bizzaro
"""
import matplotlib.pyplot as plt
import magpylib as mag3
import numpy as np
from scipy.spatial.transform import Rotation as R


#fig = plt.figure(figsize=(10,10))
'''
#2D Macro
ax1 = fig.add_subplot(2,2,1)
#3D
ax2 = fig.add_subplot(2,2,2, projection='3d')
#2D Micro
#ax3 = fig.add_subplot(3,2,3)
'''
fig = plt.figure(figsize=(5,5))
ax2 = plt.axes(projection='3d')

fig1, ax1 = plt.subplots()
fig2, ax3 = plt.subplots()

space = 120
measurement_location = [0,0,0]

mag1_strength = (0,0,100)
mag2_strength = (0,0,0)
mag3_strength = (0,0,0)
mag4_strength = (0,0,0)


#%%
#create magnet objects
EM_diamter = 6 #mm
EM_length = 40  #mm


EM1_position = (40,0,0)
EM2_position = (-40,0,0)
EM3_position = (0,40,0)
EM4_position = (0,-40,0)

EM1_orient = R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True)
EM2_orient = R.from_rotvec(-90 * np.array([0, 1, 0]), degrees=True)
EM3_orient = R.from_rotvec(-90 * np.array([1, 0, 0]), degrees=True)
EM4_orient = R.from_rotvec(90 * np.array([1, 0, 0]), degrees=True)

s1 = mag3.magnet.Cylinder(magnetization=mag1_strength , dimension=(EM_diamter,EM_length), position = EM1_position, orientation=EM1_orient)
s2 = mag3.magnet.Cylinder(magnetization=mag2_strength, dimension=(EM_diamter,EM_length), position = EM2_position, orientation=EM2_orient)
s3 = mag3.magnet.Cylinder(magnetization=mag3_strength , dimension=(EM_diamter,EM_length), position = EM3_position, orientation=EM3_orient)
s4 = mag3.magnet.Cylinder(magnetization=mag4_strength, dimension=(EM_diamter,EM_length), position = EM4_position, orientation=EM4_orient)
#c5 = mag3.current.Circular(current=0, diameter=space)

col = mag3.Collection(s1,s2,s3,s4)
mag3.display(col, axis=ax2)
#%%



#%%

#display field in xz-plane macro
xs = np.linspace(-space/2,space/2,30)
ys = np.linspace(-space/2,space/2,30)
X,Y = np.meshgrid(xs,ys)

B1 = np.array([[col.getB([x,y,0]) for x in xs] for y in ys])

U1 = [B1[:,:,0],B1[:,:,1]]
Bamp1 = np.linalg.norm(B1,axis=2)
cont1 = ax1.contourf(X,Y,Bamp1,10,cmap='rainbow')
fig2.colorbar(cont1, ax=ax1)


quiv1 = ax1.streamplot(X, Y, U1[0], U1[1], color=np.sqrt(U1[0]**2+U1[0]**2),density = 1)


ax1.set_title("100mm by 100mm ROI Magnetic Field Lines. Map in mT")
ax1.set_xlabel("x (mm)")
ax1.set_ylabel("y (mm)")
#cbar = fig1.colorbar(res.lines, ax=ax1)

#%%




#%%
#display streamplot on 3D display

lines1 = quiv1.lines.get_paths()


for line in lines1:
    old_x = line.vertices.T[0]
    old_y = line.vertices.T[1]
    # apply for 2d to 3d transformation here
    new_z = np.exp(-(old_x ** 2 + old_y ** 2) / 4)
    new_x = 1 * old_x
    new_y = 1 * old_y
    ax2.plot(new_x, new_y, new_z, 'k')
    

 

#%%

#display field in xz-plane micro


space_micro = 1 #mm
xm = np.linspace(-space_micro/2,space_micro/2,20)
ym = np.linspace(-space_micro/2,space_micro/2,20)
Xm,Ym = np.meshgrid(xm,ym)


B1 = np.array([[col.getB([x,y,0]) for x in xm] for y in ym])
U1 = [B1[:,:,0],B1[:,:,1]]

Bamp = np.linalg.norm(B1,axis=2)
cont = ax3.contourf(Xm,Ym,Bamp,100,cmap='rainbow')

quiv1 = ax3.streamplot(Xm, Ym, U1[0], U1[1], color=np.sqrt(U1[0]**2+U1[0]**2),density = 1)



ax3.set_title("1mm by 1mm ROI Magnetic Field Lines. Map in mT")
ax3.set_xlabel("x (mm)")
ax3.set_ylabel("y (mm)")
fig2.colorbar(cont, ax=ax3)


#%%
#print indivudual field strength at position
print(s1.getB(measurement_location))
ax1.plot(measurement_location[0], measurement_location[1], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=10)
ax2.plot(measurement_location[0], measurement_location[1], measurement_location[2], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=5)
ax3.plot(measurement_location[0], measurement_location[1], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=10)

#%%






