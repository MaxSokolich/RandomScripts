#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:30:05 2021

@author: bizzaro
"""
#https://magpylib.readthedocs.io/_/downloads/en/latest/pdf/
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
'''
import magpylib as mag3

import matplotlib.pyplot as plt





#%%
#Display sources, collections, paths and sensors using Matplotlib from top level functions,

src1 = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=6) 
src2 = mag3.magnet.Cylinder(magnetization=(1000,0,0), dimension=(4,5))
mag3.display(src1, src2)
#%%



# %%
#Compute the B-field of a spherical magnet at a sensor positioned at (1,2,3):
    #magpylib.getB(sources, observers, sumup=False, squeeze=True, **specs)
source = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1) 
sensor = mag3.Sensor(position=(1,2,3))
B = mag3.getB(source, sensor)
print(B)
#%%



#%%
#Compute the B-field of a spherical magnet at five path positions as seen by an observer at position (1,2,3):
    #magpylib.getB(sources, observers, sumup=False, squeeze=True, **specs)
source = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1) 
for x in [1,2,3,4,5]:
    source.move((x,0,0)) 
    B = mag3.getB(source, (1,2,3))
    print(B)
#%%


#%%
#Compute the H-field of two sources at two observer positions, with and without sumup:
    # magpylib.getH(sources, observers, sumup=False, squeeze=True, **specs)
src1 = mag3.current.Circular(current=15, diameter=2) 
src2 = mag3.misc.Dipole(moment=(100,100,100))
obs_pos = [(1,1,1), (1,2,3)]
H = mag3.getH([src1,src2], obs_pos)
print(H)

H = mag3.getH([src1,src2], obs_pos, sumup=True)
print(H)
#%%


# %%
#Sensors are observers for magnetic field computation. In this example we compute the H-field as seen by the sensor in the center of a circular current loop:
    #class magpylib.Sensor(position=(0,0,0),pixel=(0,0,0),orientation=None)
sensor = mag3.Sensor()
loop = mag3.current.Circular(current=1, diameter=1) 
H = sensor.getH(loop)
print(H)


# %%
#Field computation is performed at every pixel of a sensor. The above example is reproduced for a 2x2-pixel sensor:
sensor = mag3.Sensor(pixel=[[(0,0,0), (0,0,1)],[(0,0,2), (0,0,3)]]) 
loop = mag3.current.Circular(current=1, diameter=1)
H = sensor.getH(loop)
print(H.shape)
print(H)

#%%

#%%
#Display Magpylib objects graphically using Matplotlib:
    #display(markers=[(0, 0, 0)], axis=None, show_direction=False, show_path=True, size_sensors=1, size_direction=1, size_dipoles=1)
obj = mag3.magnet.Sphere(magnetization=(0,0,1), diameter=1)
obj.move([(.2,0,0)]*50, increment=True)
obj.rotate_from_angax(angle=[10]*50, axis='z', anchor=0, start=0,increment=True)
obj.display(show_direction=True, show_path=10)

#Display figure on your own 3D Matplotlib axis:
#my_axis = plt.axes(projection='3d') 
#%%


#%%
#With the move method Magpylib objects can be repositioned in the global coordinate system:
    #move(displacement, start=-1, increment=False)
sensor = mag3.Sensor() 
print(sensor.position) 
sensor.move((1,1,1))
print(sensor.position)


sensor.move([(1,1,1)]*4, start='append', increment=True) 
print(sensor.position)

sensor.move([(.1,.1,.1)]*5, start=2) 
print(sensor.position)


#%%
#Commands

#rotate(rotation, anchor=None, start=-1, increment=False)

#rotate_from_angax(angle, axis, anchor=None, start=-1, increment=False, degrees=True)

#class magpylib.Collection(*sources)

#remove(source)

#move(displacement, start=-1, increment=False)

#%%

#Group multiple sources in one Collection for common manipulation.
#Operations applied to a Collection are sequentially applied to all sources in the Collection. Collections do not allow duplicate sources (will be eliminated automatically).
    #class magpylib.Collection(*sources)
    

#Create Collections for common manipulation. All sources added to a Collection are stored in the sources attribute, which is an ordered set (list with unique elements only)
sphere = mag3.magnet.Sphere((1,2,3),1)
loop = mag3.current.Circular(1,1)
dipole = mag3.misc.Dipole((1,2,3))

col = mag3.Collection(sphere, loop, dipole)
print(col.sources)

#Cycle directly through the Collection sources attribute
for src in col: 
    print(src)

print(col[1])
#Add and subtract sources to form a Collection and to remove sources from a Collection.
col = sphere + loop
print(col.sources)
col - sphere
print(col.sources)
#%%

#%%
#Manipulate all objects in a Collection directly using move and rotate methods
sphere = mag3.magnet.Sphere((1,2,3),1)
loop = mag3.current.Circular(1,1)
col = sphere + loop
col.move((1,1,1))
print(sphere.position)

#compute the total magnetic field generated by the Collection at observer(1,2,3)
B = col.getB((1,2,3))
print(B)




#%%


#%%
obj = mag3.magnet.Sphere(magnetization=(0,0,1), diameter=1)
obj.move([(.2,0,0)]*50, increment=True)
obj.rotate_from_angax(angle=[10]*50, axis='z', anchor=0, start=0,increment=True)
obj.display(show_direction=True, show_path=10)

#%%


#%%
#By default a Cylinder is initialized at position (0,0,0), with unit rotation:
    #class magpylib.magnet.Cylinder(magnetization=(None, None, None), dimension=(None, None), position=(0, 0, 0), orientation=None)
magnet = mag3.magnet.Cylinder(magnetization=(100,100,100), dimension=(1,1)) 
print(magnet.position)
print(magnet.orientation.as_quat())

#Cylinders are magnetic field sources. Below we compute the H-field [kA/m] of the above Cylinder at the observer position (1,1,1),
H = magnet.getH((1,1,1))
print(H)

#or at a set of observer positions:
H = magnet.getH([(1,1,1), (2,2,2), (3,3,3)])
print(H)

#%%


#%%
#Spherical magnet with homogeneous magnetization.
    #class magpylib.magnet.Sphere(magnetization=(None, None, None), diameter=None, position=(0, 0, 0), orientation=None)

magnet = mag3.magnet.Sphere(magnetization=(100,100,100), diameter=1) 
print(magnet.position)
print(magnet.orientation.as_quat())

B = magnet.getB((1,1,1))
print(B)

B= magnet.getB([(1,1,1), (2,2,2), (3,3,3)])
print(B)
#%%

































