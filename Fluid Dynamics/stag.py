#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 18:07:56 2021

@author: bizzaro
"""
import numpy as np
import matplotlib.pyplot as plt
m = 10
theta = np.linspace(0,2*np.pi,200)
u= 2
r = (m/(2*np.pi))*((np.pi-theta)/(u*np.sin(theta)))

plt.plot(theta,r)
plt.show()