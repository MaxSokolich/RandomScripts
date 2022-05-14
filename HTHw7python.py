#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:12:53 2020

@author: bizzaro
"""
import math as math
#Parameters
l = 0.3 #m
k = 30
ro = 7900
c = 640

'''
Natural Convection
'''
hn = 10
'''
Forced Convection
'''
hf = 100
##############################################
'''
Calulate surface tempurature for 6 cases ---------- θ*s = (Ts − T∞)/(Ti − T∞), 


1) natural, t=2.5 min
2) natural, t=25 min
3) natural, t=250 min
4) forced, t=2.5 min
5) forced, t=25 min
6) forced, t=250 min

for 4 different methods
1) exact solution
2) first term of series
3) lumped capacitance
4) semi infinite solid
'''
t1 = 2.5 * 60
t2 = 25 * 60
t3 = 250 * 60
#calculate biotz numbers

biforced = (hf*l)/k

binatural = (hn*l)/k


'''
zeta and c values aquired from yaos zeta helper code
'''
# for bi = 0.1    
c1 = [1.0160942,-0.019658927,0.00502725,-0.002243,0.001264,-0.0008095,0.0005624127,0.0004132952,0.000316475894,-0.00025008]
zeta1 = [0.31105,3.17309,6.299059,9.43537,2.574323,15.7143268,18.85485954,21.995694,25.13671,28.27787]
print('for bi =0.1, zetas = ',zeta1,'c = ', c1)
# for bi = 1
c2 =[1.1191320084055834,-0.15169240233263254,0.046594006863814263,-0.02166814742980882,0.012391619995970854,-0.007992617349793682,0.005574146008049296,-0.004105883316737986,0.0031488571745335353,-0.0024908613429596833]
zeta2 = [0.860333589019956,3.425618459481836,6.437298179172701,9.529334405361848,12.645287223856226,15.771284874816157,18.902409956860264,22.036496727937937,25.172446326645396,28.309642854451006]
print('for bi =1, zetas = ',zeta2,'c = ', c2)
fo1 = 0.009889
fo2 = 0.09889
fo3 = 0.9889


'''
Exact Solution
'''
#case 1 bi = 0.1
#t= 2.5 min
thetaexact1 = 0
#t = 25 min
thetaexact2 = 0
#t = 250 min
thetaexact3 = 0

#case 2 bi = 1
#t= 2.5 min
thetaexact4 = 0
#t = 25 min
thetaexact5 = 0
#t = 250 min
thetaexact6 = 0


for i in range(len(c1)):
    thetaexact1 += c1[i]* math.exp(-(zeta1[i]**2)*fo1)*math.cos(zeta1[i])
    thetaexact2 += c1[i]* math.exp(-(zeta1[i]**2)*fo2)*math.cos(zeta1[i])
    thetaexact3 += c1[i]* math.exp(-(zeta1[i]**2)*fo3)*math.cos(zeta1[i])
    thetaexact4 += c2[i]* math.exp(-(zeta2[i]**2)*fo1)*math.cos(zeta2[i])
    thetaexact5 += c2[i]* math.exp(-(zeta2[i]**2)*fo2)*math.cos(zeta2[i])
    thetaexact6 += c2[i]* math.exp(-(zeta2[i]**2)*fo3)*math.cos(zeta2[i])
    
    
    
print('thetaexact1 = ',thetaexact1)
print('thetaexact2 = ',thetaexact2)
print('thetaexact3 = ',thetaexact3)
print('thetaexact4 = ',thetaexact4)
print('thetaexact5 = ',thetaexact5)
print('thetaexact6 = ',thetaexact6)

'''
First Term Solution
'''
print('')
print('thetafirstterm1 = ',c1[0]* math.exp(-(zeta1[0]**2)*fo1)*math.cos(zeta1[0]))
print('thetafirstterm2 = ',c1[0]* math.exp(-(zeta1[0]**2)*fo2)*math.cos(zeta1[0]))
print('thetafirstterm3 = ',c1[0]* math.exp(-(zeta1[0]**2)*fo3)*math.cos(zeta1[0]))
print('thetafirstterm4 = ',c2[0]* math.exp(-(zeta2[0]**2)*fo1)*math.cos(zeta2[0]))
print('thetafirstterm5 = ',c2[0]* math.exp(-(zeta2[0]**2)*fo2)*math.cos(zeta2[0]))
print('thetafirstterm6 = ',c2[0]* math.exp(-(zeta2[0]**2)*fo3)*math.cos(zeta2[0]))

'''
Lumped
'''
print('')
print('thetalump1 = ',math.exp((-hn*t1)/(ro*l*c)))
print('thetalump2 = ',math.exp((-hn*t2)/(ro*l*c)))
print('thetalump3 = ',math.exp((-hn*t3)/(ro*l*c)))
print('thetalump4 = ',math.exp((-hf*t1)/(ro*l*c)))
print('thetalump5 = ',math.exp((-hf*t2)/(ro*l*c)))
print('thetalump6 = ',math.exp((-hf*t3)/(ro*l*c)))

'''
Semi Infinite
'''
print('')
print('thetasi1 = ',math.exp((binatural**2)*fo1)*math.erfc(binatural*math.sqrt(fo1)))
print('thetasi2 = ',math.exp((binatural**2)*fo2)*math.erfc(binatural*math.sqrt(fo2)))
print('thetasi3 = ',math.exp((binatural**2)*fo3)*math.erfc(binatural*math.sqrt(fo3)))
print('thetasi4 = ',math.exp((biforced**2)*fo1)*math.erfc(biforced*math.sqrt(fo1)))
print('thetasi5 = ',math.exp((biforced**2)*fo2)*math.erfc(biforced*math.sqrt(fo2)))
print('thetasi6 = ',math.exp((biforced**2)*fo3)*math.erfc(biforced*math.sqrt(fo3)))
