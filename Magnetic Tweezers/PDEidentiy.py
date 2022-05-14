#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 09:32:37 2021

@author: bizzaro
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,10)
y = np.linspace(0,10)

X,Y = np.meshgrid(x,y)

u1 = (24*np.exp((2*x)+y)) - (5*(6*np.exp((2*x)+y) + (3*x*(y**2)))) + (6*np.exp((2*x)+y)) + (x*(y**3))

u2 = (x * (y**3))-(15*(x * (y**2)))

plt.figure()
plt.plot(x,u1)
plt.figure()
plt.plot(x,u2)
plt.figure()
