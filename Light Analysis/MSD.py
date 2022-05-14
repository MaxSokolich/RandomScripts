#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 17:03:09 2021

@author: bizzaro
"""
'''
TO DO:
    
    - add b4 and after light track color differences for mulitple light switches
    - add filter for best tracks (max(MSD))
    - aad total/combined MSD chart for all tracks
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

'''
TRACKMATE CSV SHOULD BE IN THE FORM 
TRACK ID        POSITION_X       POSITION_Y         FRAME
   -                -                -                 -
   -                -                -                 -
   -                -                -                 -
   -                -                -                 -
'''
data =  pd.read_csv("/Volumes/newdrive1/Tracks12_6/HEMI/SpotsHEMI1.csv")
#data =  pd.read_csv("/Volumes/newdrive1/Tracks12_6/PATCHY/SpotsAG1.csv")

frame = data['FRAME'].to_numpy(dtype='float')
ID = data['TRACK_ID'].to_numpy(dtype='float')
xdata =  data['POSITION_X'].to_numpy(dtype='float')
ydata =  data['POSITION_Y'].to_numpy(dtype='float')


#INPUTS
MSD_FILTER = 0 # filter tracks based on maximum MSD
SINGLE_TRACK_ID = 4 #indivudal track ID from trackmate CSV
SWITCH_FRAME = 140  #frame at which light is turn on






'''
this function gathers x y pos for individal tracks and plots
trck =  individual track ID --> SINGLE TRACK ID
switch frame = the frame at which the light is turned on
ax1 = track axis
ax2 = msd axis
'''
def plot_tracks(trck, switch_frame, ax1, ax2):
    #global ID
    #global xdata
    #global ydata
    
    trackX_raw = []
    trackY_raw = []
    
    '''
    pick out track data from single indivdual track
    
        trackX_raw[a][b]
        
        b: 0 or 1 --> 0 if we want trackx pos, 1 if we want frame
        a: index of either trackx or frame
    
    '''
    for i in range(len(frame)):
        if ID[i] == trck:
            
            
            x_info = [xdata[i],frame[i]]
            y_info = [ydata[i],frame[i]]
            trackX_raw.append(x_info)
            trackY_raw.append(y_info)
            
    #assign length of track to variable
    len_trck = ID.tolist().count(trck)
    
    #track x and y position lists
    trackX_pos = []
    trackY_pos = []
    
    #before light is turned on list
    before_X_pos = []
    before_Y_pos = []
    #after light is turned on list
    after_X_pos = []
    after_Y_pos = []
    

    #seperating light on light off
    
    for i in range(len_trck):
    
        trackY_pos.append(trackY_raw[i][0])
        trackX_pos.append(trackX_raw[i][0])
        
        
        if int(trackX_raw[i][1]) <= switch_frame:
            before_X_pos.append(trackX_raw[i][0])
            before_Y_pos.append(trackY_raw[i][0])
        if int(trackX_raw[i][1]) >= switch_frame:
            after_X_pos.append(trackX_raw[i][0])
            after_Y_pos.append(trackY_raw[i][0])
     
        
    
    

    T_b4 = []
    T_aft = []
    MSD_Y_before = []
    MSD_Y_after = []

    
    for i in range(1,len_trck):
        
        
        #starting position of track
        start_x = trackX_pos[0]
        start_y = trackY_pos[0]
        #next position in time
        next_x = trackX_raw[i][0]
        next_y = trackY_raw[i][0]
        #calcualte difference
        difx = next_x - start_x
        dify = next_y - start_y   
        #calcualte square difference 
        diffd = np.sqrt(difx**2+dify**2)    

   
        #Before calculations
        if trackX_raw[i][1] <= switch_frame:
            T_b4.append(i)
            MSD_Y_before.append(diffd)
        #After calculations
        if trackX_raw[i][1] >= switch_frame:
            T_aft.append(i)
            MSD_Y_after.append(diffd)
   
    #if int(max(MSD_Y_before)) > 2000 or int(max(MSD_Y_after)) > 2000:
        if diffd > MSD_FILTER:
            ax2.plot(T_b4,MSD_Y_before, color = 'k')
            ax2.plot(T_aft,MSD_Y_after, color  = 'r')
    
    
    ax1.plot(before_X_pos, before_Y_pos, color = 'k')
    ax1.plot(after_X_pos, after_Y_pos, color = 'r')

    
    
    
    
    
#initlizie figures
    
single_msd_fig = plt.figure(figsize = (20,20))
single_msd_fig, single_msd_ax = plt.subplots()
single_msd_ax.set_xlabel("T (frame)")
single_msd_ax.set_ylabel("MSD")


single_track_fig = plt.figure(figsize = (20,20))
single_track_fig, single_track_ax = plt.subplots()
single_track_ax.set_xlabel("X (px)")
single_track_ax.set_ylabel("Y (px)")



track_fig = plt.figure(figsize = (20,20))
track_fig, track_ax = plt.subplots()
track_ax.set_xlabel("X (px)")
track_ax.set_ylabel("Y (px)")

            
msd_fig = plt.figure(figsize = (20,20))
msd_fig, msd_ax = plt.subplots()
msd_ax.set_xlabel("T (frame)")
msd_ax.set_ylabel("MSD")       
        

#single track
plot_tracks(SINGLE_TRACK_ID,SWITCH_FRAME,single_track_ax,single_msd_ax)



#mulitple track
for i in tqdm(range(int(ID[-1]))):
    if ID.tolist().count(i) != 0: 
        plot_tracks(i,SWITCH_FRAME, track_ax, msd_ax)
          


'''
r = np.sqrt(xdata**2 + ydata**2)
diff = np.diff(r) #this calculates r(t + dt) - r(t)
diff_sq = diff**2
MSD = np.mean(diff_sq)
'''