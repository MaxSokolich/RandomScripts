#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:10:46 2021

@author: bizzaro
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

dyex = []
dyey = []


fig = plt.figure()
plt.xlim(0, 10)
plt.ylim(0, 10)
line1, = plt.plot(dyex, dyey, 'o')

def dye(t):
    x = 1+t
    y = 8
    dyex.append(x)
    dyey.append(y)
    line1.set_data(dyex, dyey)
    return line1


#ani = FuncAnimation(fig, dye, frames=10, interval=200)

dye = FuncAnimation(fig, dye, frames=t, interval=200)

plt.show()

