#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:28:48 2022

@author: bizzarohd
"""

import numpy as np
import sympy as sp



r, x, R, k = sp.symbols("r x R, k")

coef = r *(1+(R**2)/(r**2))



Vin  = ((-3*k*r)/(5*R))*sp.cos(x) + ((8 * k * (r**3))/(10*(R**3)))*(5*(sp.cos(x)**3) - 3*sp.cos(x))

Vout  = ((-3*k*(R**2))/(5*(r**2)))*sp.cos(x) + ((8 * k * (R**4))/(10*(r**4)))*(5*(sp.cos(x)**3) - 3*sp.cos(x))



sigma = sp.diff(Vout,r) - sp.diff(Vin,r)

sol = sp.diff(1/(r**2), r)
sp.pprint(sol)

#sp.simplify(coef)
#sp.simplify(ay)
#sp.simplify(az)
#sp.pprint(coef)
#sp.pprint(ax, "\n")
#sp.pprint(ay,"\n")
#sp.pprint(az,"\n")


#axmag=ax.subs(x,Point[0]).subs(y,Point[1]).subs(z,Point[2]).subs(t,Time)
#aymag=ay.subs(x,Point[0]).subs(y,Point[1]).subs(z,Point[2]).subs(t,Time)
#azmag=az.subs(x,Point[0]).subs(y,Point[1]).subs(z,Point[2]).subs(t,Time)


sigmaatR = sigma.subs(r,R)


sp.pprint(Vin)
sp.pprint(Vout)

sp.pprint(sigma)
sp.pprint(sigmaatR)