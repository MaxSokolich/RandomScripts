#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:59:52 2021

@author: bizzaro
"""
import magpylib as mag3
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


fig = plt.figure(figsize=(5,5))
ax = plt.axes(projection='3d')
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 1, 1]))


EM_diamter = 15 #mm
EM_length = 30  #mm
measurement_location = [0,0,0]

EM_position = (0,0,0)

orient = R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True)



s1 = mag3.magnet.Cylinder(magnetization=(0,100,0), dimension=(EM_diamter,EM_length), position = EM_position, orientation=orient)
c5 = mag3.current.Circular(current=0, diameter=50)

col = mag3.Collection(s1,c5)

mag3.display(col, axis=ax)
#plot measurment point
ax.plot(measurement_location[0], measurement_location[1], measurement_location[2], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=20, alpha=0.6)

print(s1.getB(measurement_location))

#streamplot

fig2, ax2 = plt.subplots()

xs = np.linspace(-25,25,5)
ys = np.linspace(-25,25,5)
X,Y = np.meshgrid(xs,ys)


B = np.array([[s1.getB([x,y,0]) for x in xs] for y in ys])

#display field in xz-plane using matplotlib


U = B[:,:,0]
V = B[:,:,1]
W = B[:,:,2]
ax2.streamplot(X, Y, U, V, color=np.log(U**2+V**2))
plt.show()






