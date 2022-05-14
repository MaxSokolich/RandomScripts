
'''
Compute and plot the temperature distribution 
in the composite wall for selected values of q.
What is the maximum allowable value of q? 
q vs T
'''

import math as math
import numpy as np
import matplotlib.pyplot as plt
#Define Knowns
r1 = 0.008 #m
r2 = 0.011 #m
r3 = 0.014 #m


Tinf = 600 #K
h = 2000 #W/m^2K
kt = 57 #W/mK
kg = 3 #W/mK
qdot = 100000000 #W/m^3
Rtot = 0.01847 #K/W


rthor = np.arange(r1,r2+0.001,0.001)
print(r21)
#rgrah = np.arange([r2, r3, 0.001])
#begin

qprime = qdot*math.pi*((r2**2)-(r1**2))
T2 = qprime*Rtot+Tinf
Tx = T2 + (((qdot*(r2**2))/(4*kt))*(1-(r1**2)/(r2**2)))- (((qdot*(r1**2))/(2*kt))*np.log(r2/r1))

plt.figure()
plt.plot(Tx,r21)
plt.show()