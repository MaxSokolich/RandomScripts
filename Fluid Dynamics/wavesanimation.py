
##############GENERAL
#
# --> w = np.sqrt(g*k*np.tanh(k*h))
#dxdt = (a * w * np.cosh(k*(z+h))*np.cos(k*x-w*t))/(np.sinh(h*k))
#dzdt = (a * w * np.sinh(k*(z+h))*np.sin(k*x-w*t))/(np.sinh(h*k))
#
#
#
##############DEEP WATER
#'''
#kh >> 1
#
# --> w = np.sqrt(g*k)
# --> tan(kh) ~ 1
# --> np.cosh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
# --> np.sinh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
#
#dxdt = a*w*np.exp(k*z)*np.cos(k*x-w*t)
#dzdt = a*w*np.exp(k*z)*np.sin(k*x-w*t)
#
#
#
#
##############SHALLOW WATER
#
#kh<<1
#
# --> w = np.sqrt(g*H*k)
# --> tan(kh) ~ 1
# --> np.cosh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
# --> np.sinh(k*(z+h)/(np.sinh(h*k)) ~ e^kz
# 
#dxdt = ((a*w)/(k*h))*np.cos(k*x-w*t)
#dzdt = a*w(1+(z/h))np.sin(k*x-w*t)
#
#
#
#
#
#
#
#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import solve_ivp
plt.rcParams["figure.figsize"] = (10,10)


# %%
fig = plt.figure()
ax = plt.subplot()
depth = -10
ax.set_xlim(-10,10)
ax.set_ylim(depth,10)


Final_Time =30
                                                                  #path line starting point

a =.1                                                      #wave amplitudee
wavelength = 10 #m
h = 1   

                                                     #depth of ocean
k = (2*np.pi)/wavelength
g = 9.8
omeg = np.sqrt(g*k)


x = np.linspace(-10,10, 50) #quiver plot bounds ,how postions of arrow vectors
z = np.linspace(depth,0, 50)
X,Z = np.meshgrid(x,z)

t = np.linspace(0,Final_Time, 500)

                                                                   #path line intial starting point
# %%
def velocity(t,xy):
    x = xz0[0]                                                  #xz0 is the intial starting point of the particle. this is set as the last iteration from the for loop below
    z = xz0[1]
    dxdt = (a * omeg * np.sinh(k*(z+h))*np.sin(k*x-omeg*t))/(np.sinh(h*k))
    dzdt = (a * omeg * np.sinh(k*(z+h))*np.sin(k*x-omeg*t))/(np.sinh(h*k))
    
    
    return dxdt,dzdt

#paths for variuous hiehgts
height = np.linspace(-50,0,50)

for i in height:
    xz0 = [0,i] 
    tspan_p=[0, Final_Time] #pathline time span region
    t_eval_p = np.linspace(0,Final_Time ,500) # how many points scipy integrate will evaulte
    sol_p = solve_ivp(velocity, tspan_p, xz0, t_eval = t_eval_p)
    posx = sol_p.y[0,:]
    posz = sol_p.y[1,:]
    plt.plot(posx,posz)
    plt.show()
    

# %%
                                                                   
 #Quiver
def ufield(x,z,t):
    return (a * omeg * np.cosh(k*(z+h))*np.cos(k*x-omeg*t))/(np.sinh(h*k))

def vfield(x,z,t):
    return (a * omeg * np.sinh(k*(z+h))*np.sin(k*x-omeg*t))/(np.sinh(h*k))




def update_quiver(j, ax, fig):
    u = ufield(X,Z,t[j])
    v = vfield(X,Z,t[j])
    Q.set_UVC(u, v)
    ax.set_title('$time$ = '+ str(round(t[j],3)),fontsize = 26)
    
    return Q,

def init_quiver():
    global Q
    u = ufield(X,Z,t[0])
    v = vfield(X,Z,t[0])
    Q = ax.quiver(X, Z, u, v)
    
    return  Q,
#%%












# %%
##############Streamplot

numSL = 30
Xsl   = 1*np.ones(numSL)                                                      # Streamline starting X coordinates
Ysl   = np.linspace(0,10,numSL)                                               # Streamline starting Y coordinates
XYsl  = np.vstack((Xsl.T,Ysl.T)).T 

speed = np.sqrt(ufield(X,Z,3)*ufield(X,Z,3) + vfield(X,Z,3)*vfield(X,Z,3))

ax.streamplot(X,Z,ufield(X,Z,3),vfield(X,Z,3),color=ufield(X,Z,3), arrowstyle='-')



#solve the equations for xp and yp
#pathline

#plots the particle trajctory starting at the last position in for loop above for that looped through the height.

def init_path():
        global line2
        line2, = ax.plot(posx[0],posz[0], 'o-',markersize=10)
       
        return  line2,
    
def update(i):
       
        
        line2.set_xdata(posx[i:i+1])
        line2.set_ydata(posz[i:i+1])
        return line2,
#height
inter =100  # in milliseconds how many frames per inter


# %%

#quiv = animation.FuncAnimation(fig, update_quiver, frames = range(0,len(t)),init_func=init_quiver,interval=inter,fargs=(ax, fig),repeat =False)


path = animation.FuncAnimation(fig, update, init_func=init_path,frames=range(0,len(t)),interval=inter,repeat =True)

ax.set_xlabel("x (m)")
ax.set_ylabel("z (m)")
ax.set_aspect('equal')

plt.show()
