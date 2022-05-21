#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 18:44:28 2021

@author: bizzaro
"""

#streamplot
import matplotlib.pyplot as plt
import numpy as np


fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

Xaxis = 10
Yaxis = 10
NumVectors = 20

xx = np.linspace(-10,Xaxis, NumVectors)
yy = np.linspace(-10,Yaxis, NumVectors)
XX,YY = np.meshgrid(xx,yy)

stream_time_instant1 = 0
stream_time_instant2 = 1
stream_time_instant3 = 2
stream_time_instant4 = 3


UU = XX
VV1 = -YY*stream_time_instant1
VV2 = -YY*stream_time_instant2
VV3 = -YY*stream_time_instant3
VV4 = -YY*stream_time_instant4

#speed = np.sqrt(UU**2 + VV**2)



ax1.streamplot(XX, YY, UU, VV1, density = 1)
ax1.set_title('$t$ = '+ str(stream_time_instant1)+"s")

ax2.streamplot(XX, YY, UU, VV2, density = 1)
ax2.set_title('$t$ = '+ str(stream_time_instant2)+"s")

ax3.streamplot(XX, YY, UU, VV3, density = 1)
ax3.set_title('$t$ = '+ str(stream_time_instant3)+"s")

ax4.streamplot(XX, YY, UU, VV4, density = 1)
ax4.set_title('$t$ = '+ str(stream_time_instant4)+"s")

for ax in fig1.get_axes():
    ax.label_outer()

