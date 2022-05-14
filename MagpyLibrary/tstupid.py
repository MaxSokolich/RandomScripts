#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 20:36:49 2021

@author: bizzaro
"""
import numpy as np
perm = 1.26*(10**(-4))
perm0 = 4*np.pi *(10**(-7))

num_loops_D = 5
num_loops_L = 12

N = 5
space = 100
L = .03
coil1_current = 1

magnitization1 = ((coil1_current*N)/L)*(100-1)#

M = ((perm/perm0)-1)*((N*coil1_current)/L)

print(magnitization1)
print(M)


B=.418*2*3.14*.01**3*100
print(B)