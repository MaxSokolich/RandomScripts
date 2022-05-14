#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 08:32:42 2020

@author: bizzaro
"""

'''
Diffie and Hellman

g = 27, working module 677

choose a secret exponent
n = 131

N = g**n mod 677

so calculate 27**131 mod 677

---------------------------------------------------------

first we calculate powers of g mod 677

g^2^0 = g^1 = 27 mod 677 = 27
g^2^1 = 27^2 = 729 mod 677  = 52
g^2^2 = 52^2 = 2704 mod 677 = 673 = -4
g^4^2 = g^8 = (-4)^2 = 16 mod 677 = 16
g^8^2 = g^16 = 256
g^32 = 256^2 = 65536 mode 677 = 544
g^64 = g^32^2 = 544^2 = 295936 mod 677 = 87
g^128 = g^64^2 = 87 ^2 = 7569 mod 677 = 122

    idea behind quick exponential calculations if to use repeated squaring 
    method to calculate g^131 mod 677.

    changes 130 muliplications to log2 131 mulitplcations  = 8.

    131 = 2^7 + 2^1 + 2^0 = 128+2+1 =131

    write your n in base 2

    now g^131 mod 677 = g^128 * g^2 * g^1 = 122 #52 *27 mode 677 = 171288 mod 677 = 7

    so N = g^131 mod 677 = 7

    that completes step 3

step 4:
    ---> send to your partner N
    <--- partner sends you their M

step 5:

    calculate K = M^n mod 677

    so k = M^131 mod 677

    at this point both you and your partner should have the same K
    dont check though at this point, dont share the private key over a public network

step 6:

    convert DELAWARE to numbers
    the process is to take two characters at a time and convert them using base 26.
    A = 0, B =1, C = 2 etc

    DE = (34) base 26 = 4 *26^0 + 3*26^1 = 82 = M1
    etc

Encryption:
    to encrypt M1 you simply multiply M! by K mod 677
    
    C1 = K*M1 mod 677
    C2 = K*M2 mod 677
    C3 =
    C4 = 
    
    dont check that you each get the same M!, M2, M3, M4
    check Ci instead
    if they all match then youre both all good



This is all he is asking us to do
Submission:
    who partner was
    secret expnent n
    capital K
    M1-M4
    C1-C4

---------------------------------
'''
g = 27
p = 677

#step 1
#partner = Dylan Frasher

print('Partner = Dylan Frasher')

#step 2

n = 278
print('n = ', n)

#step 3
#calculate N = g^n mod p

N = (g**n)%p
print('N = ', N)


#step 4
#dylans M = 
M = 57

K = (M**n)%p
print('K = ', K )

#step 6
#encrypt DELAWARE
#base26

D = 3
E = 4
L = 11
A = 0
W = 22
A = 0
R = 17
E = 4

DE = 3 * 26 + 4
LA = 11 * 26 + 0
WA = 22 * 26 + 0
RE = 17 * 26 +4
print(DE,'-',LA,'-',WA,'-',RE)
print('m1 = ', DE)
print('m2 = ', LA)
print('m3 = ', WA)
print('m4 = ', RE)
m1 = DE
m2 = LA
m3 = WA
m4 = RE


#step 7
#ecnvrypt delaware

c1 = (K*m1)%p
c2 = (K*m2)%p
c3 = (K*m3)%p
c4 = (K*m4)%p

print('c1 = ', c1)
print('c2 = ', c2)
print('c3 = ', c3)
print('c4 = ', c4)
















