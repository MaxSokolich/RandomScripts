#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 09:39:30 2021

@author: bizzaro
"""
import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(1,10,30)





x0 = 1
y0 = 8
time = np.linspace(0,2,20)
yp = []
for t in time:
    y = (y0/(x0**(-t))*(x**(-t)))
    yp.append(y)

fig = plt.figure()
plt.xlim(0,10)
plt.ylim(0,10)
plt.plot(x,y)
plt.show()

