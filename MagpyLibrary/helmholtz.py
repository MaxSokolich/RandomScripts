#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 13:52:45 2021

@author: bizzaro
"""
'''
mag1_strength = (0,0,(100*c1.getB(40,0,0)[0]))
mag2_strength = (0,0,(100*c1.getB(-40,0,0)[0]))
mag3_strength = (0,0,(100*c1.getB(0,40,0)[0]))
mag4_strength = (0,0,(100*c1.getB(-0,-40,0)[0]))


http://www.emagtech.com/wiki/index.php/EM.Ferma_Tutorial_Lesson_5:_Modeling_Solenoids_%26_Toroidal_Coils
'''
import numpy as np
import magpylib as mag3
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(10,10))
ax2 = plt.axes(projection='3d')

fig1, ax1 = plt.subplots()

fig2 = plt.figure(figsize=(10,10))
ax3 = plt.axes(projection='3d')

fig3, ax4 = plt.subplots()



coil1_current = 2
L = .01
space =100
num_loops_D = 10
num_loops_L = 10
N = num_loops_L*num_loops_D

coil1 = [[mag3.current.Circular(current=coil1_current, diameter=h,position = (0,0,z-20)) for z in np.linspace( 0,L*1000,num_loops_L)] for h in np.linspace(80,100,num_loops_D)]
coil2 = [[mag3.current.Circular(current=coil1_current, diameter=h,position = (0,0,z+20)) for z in np.linspace( 0,L*1000,num_loops_L)] for h in np.linspace(80,100,num_loops_D)]

# magnetic microsphere
sphere = mag3.magnet.Sphere(magnetization=(0,0,10), diameter=0.023)
c5 = mag3.current.Circular(current=0, diameter=.1)

col = mag3.Collection(coil1,coil2,sphere)
col2 = mag3.Collection(c5,sphere)

measurement_location = [0,0,10]
print(col.getB(measurement_location))

mag3.display(col, axis=ax2)


xs = np.linspace(-space/2,space/2,40)
ys = np.linspace(-space/2,space/2,40)
zs = np.linspace(-space/2,space/2,40)
X,Z = np.meshgrid(xs,zs)

B = np.array([[mag3.getB(col,[x,0,z],sumup=False) for x in xs] for z in zs])
#contour
Bamp = np.linalg.norm(B,axis=2)
cont = ax1.contourf(X,Z,Bamp,cmap='rainbow')
fig1.colorbar(cont, ax=ax1)

#streamplot
U = B[:,:,0]
V = B[:,:,1]
W = B[:,:,2]

res = ax1.streamplot(X, Z, U, W,color=np.sqrt(U**2+W**2),density = 1)
ax1.set_title("100mm by 100mm ROI Magnetic Field Lines. Map in mT")
ax1.set_xlabel("x (mm)")
ax1.set_ylabel("z (mm)")


lines1 = res.lines.get_paths()


for line in lines1:
    old_x = line.vertices.T[0]
    old_y = line.vertices.T[1]
    # apply for 2d to 3d transformation here
    new_z = np.exp(-(old_x ** 2 + old_y ** 2) / 4)
    new_x = 1 * old_x
    new_y = 1 * old_y
    ax2.plot(new_x, new_z, new_y, 'b')

#################################################################################
#

space_micro = .1 #mm
xm = np.linspace(-space_micro/2,space_micro/2,40)
ym = np.linspace(-space_micro/2,space_micro/2,40)
zm = np.linspace(-space_micro/2,space_micro/2,40)
Xm,Zm = np.meshgrid(xm,zm)

Bm = np.array([[col.getB([x,0,z]) for x in xm] for z in zm])

#contour plot
Bampm = np.linalg.norm(Bm,axis=2)
contm = ax4.contourf(Xm,Zm,Bampm,cmap='rainbow')
fig3.colorbar(contm, ax=ax4)


#streamplot
Um = Bm[:,:,0]
Vm = Bm[:,:,1]
Wm = Bm[:,:,2]

resm = ax4.streamplot(Xm, Zm, Um, Wm, color=np.sqrt(Um**2+Wm**2),density = 1)
lines2 = resm.lines.get_paths()

mag3.display(col2, axis=ax3)
circle1 = plt.Circle((0, 0), 0.023, color='k')
ax4.add_patch(circle1)
for line in lines2:
    old_x1 = line.vertices.T[0]
    old_y1 = line.vertices.T[1]
    # apply for 2d to 3d transformation here
    new_z1 = np.zeros([2,])#np.sqrt((old_x1 ** 2 + old_y1 ** 2) / 4)
    new_x1 = 1 * old_x1
    new_y1 = 1 * old_y1
    ax3.plot(new_x1, new_z1, new_y1, 'b')
    
    
    
ax4.set_title("100um by 100um ROI Magnetic Field Lines. Map in mT")
ax4.set_xlabel("x (mm)")
ax4.set_ylabel("z (mm)")


plt.show()
