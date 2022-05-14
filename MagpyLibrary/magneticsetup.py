#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:06:56 2021

@author: bizzaro
"""
'''
Magpylib uses units of
• [mT]: for the B-field and the magnetization (mu0*M). • [kA/m]: for the H-field.
• [mm]: for all position inputs.
• [deg]: for angle inputs by default.
• [A]: for current inputs.

# magnets
src1 = mag3.magnet.Box(magnetization=(0,0,1000), dimension=(1,2,3))
src2 = mag3.magnet.Cylinder(magnetization=(0,1000,0), dimension=(1,2)) 
src3 = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1)

# currents
src4 = mag3.current.Circular(current=15, diameter=3)
src5 = mag3.current.Line(current=15, vertices=[(0,0,0), (1,2,3)]) 

# misc
src6 = mag3.misc.Dipole(moment=(100,200,300))

#magpylib.getB(sources, observers, sumup=False, squeeze=True, **specs)
ax.axes.set_xlim3d(left=0, right=10) 
ax.axes.set_ylim3d(bottom=0, top=10) 
ax.axes.set_zlim3d(bottom=0, top=10) 
'''

#class magpylib.magnet.Cylinder(magnetization=(None, None, None), dimension=(None, None), position=(0, 0, 0), orientation=None)
#display(markers=[(0, 0, 0)], axis=None, show_direction=False, show_path=True, size_sensors=1, size_direction=1, size_dipoles=1)

import magpylib as mag3
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#fig = plt.figure(figsize=(10,10))
#ax = plt.axes(projection='3d') 



s1 = mag3.magnet.Cylinder(magnetization=(0,0,100), dimension=(15,35), position = (35,0,0),orientation=R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True)) 
s2 = mag3.magnet.Cylinder(magnetization=(0,0,0), dimension=(15,35), position = (-35,0,0),orientation=R.from_rotvec(90 * np.array([0, 1, 0]), degrees=True))
s3 = mag3.magnet.Cylinder(magnetization=(0,0,0), dimension=(15,35), position = (0,35,0),orientation=R.from_rotvec(90 * np.array([1, 0, 0]), degrees=True)) 
s4 = mag3.magnet.Cylinder(magnetization=(0,0,0), dimension=(15,35), position = (0,-35,0),orientation=R.from_rotvec(90 * np.array([1, 0, 0]), degrees=True))
c5 = mag3.current.Circular(current=0, diameter=35)
col = mag3.Collection(s1,s2,s3,s4,c5)

xs = np.linspace(-40,40,10)
ys = np.linspace(-40,40,10)
print(s1.getB([35,0,0]))


B = np.array([[col.getB([x,y,0]) for x in xs] for y in ys])
fig2, ax = plt.subplots()
X,Z = np.meshgrid(xs,ys)
U,V = B[:,:,0], B[:,:,2]
ax.streamplot(X, Z, U, V, color=np.log(U**2+V**2), density=2)
plt.show()

ax = mag3.display(col)


plt.show()
