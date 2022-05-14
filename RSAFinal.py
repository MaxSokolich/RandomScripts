#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:53:09 2020

@author: bizzaro
"""

p = 5
q = 137
n = 685
e = 121
#choose an interger relatively prime to (p-1)(q-1)     
#thus need to solve 121d = 1 mod (p-1)(q-1)  

b = (p-1)*(q-1)  
b = 544

#Step 1:


import math as math
import string
    
def Euclidean(b,e, verbose=True): #Eulcidean Algorithm to show gcd(544,121) = 1
    if b < e:
        return Euclidean(b,e, verbose)
    print()
    while e != 0:
        if verbose: print('%s = %s * %s + %s' % (b, math.floor(b/e), e, b % e))
        (b,e) = (e, b%e)
    if verbose:
        print('GCD = %s' % b)
        
#Euclidean(b,e)       

def egcd(e, b): #where e = 121, b = 544
    #solves for constants x and y in 121*x + 544*y = 1 = gcd(121,544)
    x,y, u,v = 0,1, 1,0
    while e != 0:
        q, r = b//e, b%e
        m, n = x-u*q, y-v*q
        b,e, x,y, u,v = e,r, u,v, m,n
    gcd = b
    return gcd, x, y
#print(egcd(e,b))
d = 9
print('d = ', d)



def decrypt():
   
    #convert letter pairs into numbers
    CE = 2 * 26 + 4
    MJ = 12 * 26 + 9
    GP = 6 * 26 + 15
    print('CEMJGP = ', CE,'-',MJ,'-',GP)
    
    #decrypt function
    ci= [CE, MJ, GP]
    mi = []

    for i in range(len(ci)):
        m = (ci[i]**d) % (p*q)
        mi.append(m)
    print('mi = ', mi) 
    
    #convert each number back into characters
    x1 = 7
    x2 = 1
    x3 = 17

    y1 = mi[0] - x1 * 26 
    y2 = mi[1] - x2 * 26  
    y3 = mi[2] - x3 * 26 
    
    num2alpha = dict(zip(range(0, 26), string.ascii_uppercase))
    print('Decrypted Message  = ', num2alpha[x1],num2alpha[y1],num2alpha[x2],num2alpha[y2],num2alpha[x3],num2alpha[y3])

decrypt()

















