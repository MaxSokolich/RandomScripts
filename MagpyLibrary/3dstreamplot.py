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
from matplotlib import gridspec

fig = plt.figure(figsize=(10,8))
gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 

ax1 = fig.add_subplot(3,2,1)
ax2 = fig.add_subplot(3,2,2, projection='3d')




#3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

#%%
#Create magnet objects

EM_diamter = 15 #mm
EM_length = 30  #mm
measurement_location = [0,15,0]

EM_position = (0,0,0)

orient = R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True)
s1 = mag3.magnet.Cylinder(magnetization=(0,0,100), dimension=(EM_diamter,EM_length), position = EM_position, orientation=orient)
c5 = mag3.current.Circular(current=0, diameter=80)
col = mag3.Collection(s1,c5)
#%%



#%%
#display field in xy-plane macro

xs = np.linspace(-25,25,5)
ys = np.linspace(-25,25,5)
X,Y = np.meshgrid(xs,ys)

B = np.array([[s1.getB([x,y,0]) for x in xs] for y in ys])

U = B[:,:,0]
V = B[:,:,1]
W = B[:,:,2]

res = ax1.streamplot(X, Y, U, V, color=np.log(U**2+V**2),density = 1)
cbar = fig.colorbar(res.lines, ax=ax1)
lines = res.lines.get_paths()
#%%


#%%


#%%
#display streamplot on 3D display
mag3.display(col, axis=ax2)

for line in lines:
    old_x = line.vertices.T[0]
    old_y = line.vertices.T[1]
    # apply for 2d to 3d transformation here
    new_z = np.exp(-(old_x ** 2 + old_y ** 2) / 4)
    new_x = 1.2 * old_x
    new_y = 0.8 * old_y
    ax2.plot(new_x, new_y, new_z, 'k')
#%%






#%%
#print indivudual field strength at position
ax1.plot(measurement_location[0], measurement_location[1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=20, alpha=0.6)
print(s1.getB(measurement_location))
#%%










