#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:22:50 2021

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
#imports
import magpylib as mag3
source = mag3.magnet.Cylinder(magnetization=(0,0,350), dimension=(4,5)) 
observer_pos = (4,4,4)
print(source.getB(observer_pos)) #source.getB(observer_pos)  -->   gets magnetic field vector at the observer position