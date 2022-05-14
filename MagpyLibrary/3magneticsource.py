#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:23:43 2021

@author: bizzaro
"""
#https://magpylib.readthedocs.io/_/downloads/en/latest/pdf/
'''
Magpylib uses units of
• [mT]: for the B-field and the magnetization (mu0*M). • [kA/m]: for the H-field.
• [mm]: for all position inputs.
• [deg]: for angle inputs by default.
• [A]: for current inputs.

'''
import magpylib as mag3
 # magnets
src1 = mag3.magnet.Box(magnetization=(0,0,1000), dimension=(1,2,3))
src2 = mag3.magnet.Cylinder(magnetization=(0,1000,0), dimension=(1,2)) 
src3 = mag3.magnet.Sphere(magnetization=(1000,0,0), diameter=1)

# currents
src4 = mag3.current.Circular(current=15, diameter=3)
src5 = mag3.current.Line(current=15, vertices=[(0,0,0), (1,2,3)]) 
# misc
src6 = mag3.misc.Dipole(moment=(100,200,300))

# sensor
sens = mag3.Sensor()
for obj in [src1, src2, src3, src4, src5, src6, sens]: 
    print(obj)
    
'''
All Magpylib objects are endowed with position and orientation attributes 
that describe their state in a global coordinate system. By default they are
 set to zero and unit-rotation respectively.
'''