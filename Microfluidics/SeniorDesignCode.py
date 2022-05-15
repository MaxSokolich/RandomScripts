#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:37:27 2020

@author: bizzaro
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:06:09 2020

@author: bizzaro
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:14:44 2020

@author: bizzaro
"""
import cv2
import numpy as np
import imutils
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist
import csv

#these are variables user would have to change depending on the video 

videoM  = "cleartape.MOV"   # video input file for mother dropelts
videoD = "spltingT.mov"     #video input file for daughter droplets




Q = input("M or D")
if Q == "M" or Q == 'm':
    outputfile = "Mother.csv" # name of output csv file to write the data to
    fiducial = 1 # size in mm of height of frame from fiducial markings
    colorlowerbound = [10,25,25] #lower blue detection bound / change this depending on the color of the dropelt
    colorupperbound = [120,255,255] #upper blue detection bound
    '''
    if centroid passes purple line, add 1 to count
    if centroid is within yellow lines, start calculating area
    if centroid is within red lines, calcualate distance between centroids
    black lines represent pixel to metric reference distance. we know channel width is 1 mm, find the distance in pixels and use that is scale
    '''
    cap = cv2.VideoCapture(videoM)
    #cap = cv2.VideoCapture("largedropclear.MOV")
    #cap.set(1,150)
    totalframes = cap.get(7)
    fps = cap.get(5)
    duration = totalframes/fps # computes the length of the video based on how many frames are present and the fps of the video
    print('This video is', round(duration,2), 'seconds long')
    #minpixelarea = 30000 # change this to remove small areas that would interfere with the droplet area
    #distance line filter. match these fractions to the width of the channel
    #dont need this if using fiducials
    hy1 = 1/3 
    hy2 = 5.5/7
    ay1 = 1/3
    ay2 = 2/3
    area_list = [] # the area of a droplet every frame, and if a droplet is not present add 0
    splitarea = [] #this splits the list above into a nest list of all the areas forå 1 droplet
    avg_area_list = []
    per_list = []
    splitper =[]
    avg_per_list = []
    dist_list = []
    splitdist = []
    avg_dist_list = []
    framecount = [] 
    finalframecount = []
    vellist = []
    EntranceCounter = 0
    intvl = 1 # determines how the intervala t which the program reads and anlzys frames
    framelist = np.arange(0, totalframes, intvl) # an array in range from 0 to the totall number of frames in the video
    #midoint function. calcualtes the midpoint given 2 points and their corodinates
    def midpoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
    colorlowerbound = [10,25,25] #lower blue detection bound
    colorupperbound = [120,255,255] #upper blue detection bound
    #begin looping through every frame
    for i in framelist:
        _ , frame = cap.read()
        f = frame.copy()
        cap.set(1, i)
        if frame is None:
            break
        print(i,'/',totalframes)
        #resize the frames to fit in window
        scale_percent = 60
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame = cv2.resize(frame, dsize)
        minpixelarea = (frame.shape[0]*frame.shape[1])/15 # this should be a little less than the area being calculated
        #copys the oringal video for mark up later
        f = frame.copy()
        fc = f[:frame.shape[1], 0:int(frame.shape[1]/2)]# new frame crop for single droplet
        f2 = fc.copy()
        # blurs the frame 
        frame = cv2.blur(frame,(20,20))
        fc = cv2.blur(fc, (20,20))
        #converts frame from blue green red to hue saturation value
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(fc, cv2.COLOR_BGR2HSV)
        #determine upper and lower bounds for detectiing color
        lower = np.array(colorlowerbound) #10,25,25]) lower blue
        upper = np.array(colorupperbound)#120,255,255]) upper blue
        mask = cv2.inRange(hsv, lower, upper)
        mask2 = cv2.inRange(hsv2, lower, upper)
        m2 = mask2.copy()
        res = cv2.bitwise_and(f2,f2, mask = mask2)
        #start finding contours for distance iamge
        cnts =  cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cnts = imutils.grab_contours(cnts)
        (cnts, _) = contours.sort_contours(cnts)
        #start finding contours for single image
        cnts2 =  cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cnts2 = imutils.grab_contours(cnts2)
        #counter crosing lines purple
        start = (int(f2.shape[1]/2), 0)
        end = (int(f2.shape[1]/2) , int(f2.shape[0]))
        #cv2.line(f2, start, end,(255, 0, 255), 2) 
        #draws lines for area bounding lines
        #cv2.line(f2, (int(f2.shape[1]*(ay1)),0),(int(f2.shape[1]*(ay1)),int(f2.shape[0])),(0, 255, 255), 2) #area exit line
        #cv2.line(f2, (int(f2.shape[1]*(ay2)),0),(int(f2.shape[1]*(ay2)),int(f2.shape[0])),(0, 255, 255), 2) #area entrance line
        #pixel to metric refence length bounding lineslines
        tstart=(0,int(frame.shape[0]*(hy1)))
        tend = (int(frame.shape[1]),int(frame.shape[0]*(1/3)))
        bstart= (0,int(frame.shape[0]*(hy2)))
        bend=(int(frame.shape[1]),int(frame.shape[0]*(5.5/7)))
        cv2.line(f, tstart,tend,(0, 0, 0), 2) #top line
        cv2.line(f, bstart,bend,(0, 0, 0), 2) #bottom line
        #computes the distance between the top channel line and bottom channel line
        refdist =  (bstart[1] - tstart[1])
        #refdist stuff
        #only need this if using fiducials
        #change to widht for fidicuals since wont be able to mark across the channel
        pixeldist = frame.shape[1]
        scale = fiducial/refdist # mulitply any measurment in pixels by this scale number
        area = 0
        refObj = None
        secondcirclecolor = (10,255,0)
        firstcirclecolor = (255,255,0)
        area2 = 0
        perimeter = 0
        for c in cnts2:
            if cv2.contourArea(c) > 0:
                perimeter += cv2.arcLength(c,True)
               
                area2 += cv2.contourArea(c)
                cv2.drawContours(f2,[c], -1,(0,0,0),2)
        #print(perimeter*scale)
        if area2 > minpixelarea:
            M = cv2.moments(mask2)
            if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(f2, (cx,cy),3, (255,255,255), -1)
                cv2.putText(f2, "Centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            #print(cx,cy)
            else:
                center = 0,0 
            absdistance = abs(cx-f2.shape[1]/2)
            #print(absdistance)
            if (absdistance <= 20):
                framecount.append(int(i))
                EntranceCounter +=1
                #print(framecount)
            if cx < int(f2.shape[1]*(ay2)) and cx > int(f2.shape[1]* (ay1)):
                per_list.append(perimeter)
                area_list.append(area2)
                #print(area_list)
                #print(per_list)
            else:
                area_list.append(0)
                per_list.append(0)
                #print(area_list)
                #print(per_list)
            cv2.putText(f2, "Avg Area: {}mm".format(str(area2*(scale**2))), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2)
            cv2.putText(f2, "Avg Perimeter: {}mm".format(str(perimeter*(scale))), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2)
        for c in cnts:
            if cv2.contourArea(c) > minpixelarea:
                area += cv2.contourArea(c)
                cv2.drawContours(f,[c], -1,(0,0,0),2)
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int") 
                box = perspective.order_points(box)
        # compute the center of the bounding box
         #finds center of bounding box by taking average of boundbox in both x and y direction
                cX = int(np.average(box[:, 0]))  #another way of finding the centroid, finds teh center of the bounding box
                cY = int(np.average(box[:, 1]))
                if refObj is None:
                    (tl, tr, br, bl) = box
                    (tlblX, tlblY) = midpoint(tl, bl) #midpoint of right edge of bounding box
                    (trbrX, trbrY) = midpoint(tr, br)  #midpoint of left edge of bounding box
                    D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                    refObj = (box, (cX,cY), D)#/.955) # add D/width of left most obect in real life (inches)
                  # reference object is 3 tuple of(sorted coords, centroid of reference object, pixels per metric ratio)
                    continue
                cv2.drawContours(f,[box.astype('int')], 0, secondcirclecolor,2) #(10,255,0) = neon green #draws the contours on the origanl image frame in neon green
                cv2.drawContours(f, [refObj[0].astype("int")], -1, firstcirclecolor, 2)
                refCoords = np.vstack([refObj[0], refObj[1]])
                objCoords = np.vstack([box, (cX, cY)])
                #first and second cicles centroids
                firstcircleX = refCoords[4][0]
                firstcircleY = refCoords[4][1]
                secondcircleX = objCoords[4][0]
                secondcircleY = objCoords[4][1]
                (srx,sry) = midpoint((objCoords[1][0],objCoords[1][1]),(objCoords[2][0],objCoords[2][1])) # midpoint of second dropelts right edge
                if trbrX > int(frame.shape[1]*0) and srx < int(frame.shape[1]):
                    cv2.circle(f, (int(trbrX),int(trbrY)),9, (0,0,0), -1) 
                    cv2.circle(f, (int(srx),int(sry)),9, (0,0,0), -1) 
                    D = dist.euclidean((trbrX, trbrY), (srx, sry))
                    (mX, mY) = midpoint((trbrX, trbrY), (srx, sry))    
                    cv2.putText(f, "{:.1f}mm".format(D*scale), (int(mX), int(mY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,0), 2)   
                    cv2.circle(f, (cX,cY),3, (255,255,255), -1)
                    cv2.putText(f, "Centroid", (cX-20,cY-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                    cv2.circle(f, (int(firstcircleX),int(firstcircleY)),4, firstcirclecolor, -1) #draws midpoint of right edge of bounding box
                    cv2.circle(f, (int(secondcircleX),int(secondcircleY)),4, secondcirclecolor, -1) #draws midpoint of right edge of bounding box 
                    cv2.line(f, (int(trbrX), int(trbrY)), (int(srx), int(sry)),(0, 0, 255), 2) 
                    dist_list.append(D)
        if area < minpixelarea*1.5:
            dist_list.append(0)
        # 1 mm  = 263 pixel
        numpy_horizontal = np.hstack((f2, res))
        numpy_vertical = np.vstack((f, numpy_horizontal))
        cv2.imshow('im3', numpy_vertical)
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            cap.release()
    for i in range(len(dist_list)):
        if dist_list[i-1] == 0 and dist_list[i] !=0:
           splitdist.append(dist_list[i:i+2])
    for i in range(len(splitdist)):
        mmavg = (sum(splitdist[i])/len(splitdist[i]))*scale
        avg_dist_list.append(round(mmavg,2))
    for i in range(len(area_list)):
        if area_list[i-1] == 0 and area_list[i] !=0:
            splitarea.append(area_list[i:i+8])
    for i in range(len(splitarea)):
        mmavg = (sum(splitarea[i])/len(splitarea[i]))*(scale**2)
        avg_area_list.append(round(mmavg, 2))
    for i in range(len(per_list)):
        if per_list[i-1] == 0 and per_list[i] !=0:
            splitper.append(per_list[i:i+8])
    for i in range(len(splitper)):
        mmavg = (sum(splitper[i])/len(splitper[i]))*(scale)
        avg_per_list.append(round(mmavg, 2))
    avgdist = sum(avg_dist_list)/len(avg_dist_list)
    avgarea = sum(avg_area_list)/len(avg_area_list)
    avgper = sum(avg_per_list)/len(avg_per_list)
    # finding velcoty based on # of frames counted between droplets
    a = np.array(framecount)
    lst1 = np.diff(a)
    finalframecount = []
    for i in range(len(lst1)):
        if lst1[i] > 5:
             finalframecount.append(lst1[i])
    for i in range(len(finalframecount)):
        vel = (fps/finalframecount[i])* avgdist
        vellist.append(round(vel,2))
    avgframe = sum(finalframecount)/len(finalframecount)
    avgvel = (fps/avgframe)* avgdist
    #print("average number of frames between each droplet = ", avgframe, 'frames')
    print('======PERIMETER STATS======')
    print("perimeter of each droplet = ", avg_per_list)
    print("average velocity of droplet = ", round(avgper,2), 'mm\n')
    print('======VELOCITY STATS======')
    print("velocity of each droplet = ", vellist)
    print("average velocity of droplet = ", round(avgvel,2), 'mm/s\n')
    print('======DISTANCE STATS=======')
    print('average distance between droplets list = ', avg_dist_list)
    print('average distance between droplets  = ', round(avgdist, 2), 'mm\n')
    print('======AREA STATS========')
    print('average dropelt area list = \n', avg_area_list)
    print('average droplet area = ', round(avgarea, 2), 'mm^2\n')
    print('=======COUNTING STATS=======')
    print('# areas measured = ', len(avg_area_list))
    print('# of droplet detected from counter = ', EntranceCounter) 
    print('# distances measured =', len(avg_dist_list))
    print('number of droplets from frame count/velocity = ', len(finalframecount)) 
    video_dict = {"velocity of each droplet list" : vellist,
                  "average droplet area list" : avg_area_list,
                  "average distance between droplets list" : avg_dist_list,
                  "average droplet perimeter list" : avg_per_list
        }
    print(video_dict)
    with open(outputfile, "w") as f:
        for key in video_dict.keys():
            f.write("%s,%s\n"%(key,video_dict[key]))
elif Q == "D" or Q == 'd':
    outputfile = "Daughter.csv"
    cap = cv2.VideoCapture(videoD)
    #cap.set(1,90)
    totalframes  = cap.get(7)
    print(totalframes)
    minpixelarea = 2000
    colorlowerbound = [0,15,20] #[0,25,25] [0,0,25][73,37,74] -------------------- [0,15,20] for T ----------- [0,0,80] for Y
    colorupperbound = [20,200,200] #[20,200,255][25,25,255][93,74,154] ---------------- [20,200,200] for T ---------- [40,255,255] for Y 
    lower = np.array(colorlowerbound) #10,25,25]) lower blue
    upper = np.array(colorupperbound)
    area_list_top = [] #this calcualtes the area of a droplet every frame, and if a droplet is not present add 0
    splitareatop = [] #this splits the list above into a nest list of all the areas of 1 droplet
    avg_area_list_top = []
    area_list_bottom = [] #this calcualtes the area of a droplet every frame, and if a droplet is not present add 0
    splitareabottom = [] #this splits the list above into a nest list of all the areas of 1 droplet
    avg_area_list_bottom = []
    topline =  1/3 #1/3 for T--------- 1/2 for Y
    bottomline = 2/3 #2/3 for T----------2/3 for Y
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        print(frame.shape)
        #print(frame.shape)
        scale_percent = 40
        ftop = frame[0:int(frame.shape[0]*(2/4)),:frame.shape[1]]
        widtht = int(ftop.shape[1] * scale_percent / 100)
        heightt = int(ftop.shape[0] * scale_percent / 100)
        dsizet = (widtht, heightt)
        ftop = cv2.resize(ftop, dsizet)
        ft = ftop.copy()
        cv2.line(ft, (0,int(ftop.shape[0]*(topline))),(int(ftop.shape[1]),int(ftop.shape[0]*(topline))),(0, 255, 255), 2) #area exit line
        cv2.line(ft, (0,int(ftop.shape[0]*(bottomline))),(int(ftop.shape[1]),int(ftop.shape[0]*(bottomline))),(0, 255, 255), 2) 
        ftop = cv2.blur(ftop, (20,20))
        hsvtop = cv2.cvtColor(ftop, cv2.COLOR_BGR2HSV)
        masktop = 255 - cv2.inRange(hsvtop, lower, upper)
        cntstop =  cv2.findContours(masktop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cntstop = imutils.grab_contours(cntstop)
        '''
        canny = cv2.Canny(ftop, 0, 152)
        canny = cv2.dilate(canny, None, iterations=5)
        canny = cv2.erode(canny, None, iterations=5)
        '''
        fbottom = frame[int(frame.shape[0])- int(frame.shape[0]/2):, :frame.shape[1]]
        widthb = int(fbottom.shape[1] * scale_percent / 100)
        heightb = int(fbottom.shape[0] * scale_percent / 100)
        dsizeb = (widthb, heightb)
        fbottom = cv2.resize(fbottom, dsizeb)
        fb = fbottom.copy()
        cv2.line(fb, (0,int(fbottom.shape[0]*(topline))),(int(fbottom.shape[1]),int(fbottom.shape[0]*(topline))),(0, 255, 255), 2) #area exit line
        cv2.line(fb, (0,int(fbottom.shape[0]*(bottomline))),(int(fbottom.shape[1]),int(fbottom.shape[0]*(bottomline))),(0, 255, 255), 2) 
        fbottom = cv2.blur(fbottom, (20,20))
        hsvbottom = cv2.cvtColor(fbottom, cv2.COLOR_BGR2HSV)
        maskbottom = 255 - cv2.inRange(hsvbottom, lower, upper)
        cntsbottom =  cv2.findContours(maskbottom, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cntsbottom = imutils.grab_contours(cntsbottom)
        #res = cv2.bitwise_and(ftop,ftop, mask = 255 - masktop)
        framearea = ftop.shape[0] *ftop.shape[1]
        areatop = 0
        areabottom = 0
        for c in cntstop:
            if cv2.contourArea(c) > minpixelarea:
                #masktop = np.zeros( (200,200) )
                #cv2.fillPoly(masktop, pts =[c], color=(255,255,255))
                areatop += cv2.contourArea(c)
                #cv2.drawContours(ft,[c], -1,(0,0,0),2)
                M = cv2.moments(c)
                #if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(ft, (cx,cy),3, (255,255,255), -1)
                cv2.putText(ft, "Centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                if cy > int(ftop.shape[0]*(1/3)) and cy < int(ftop.shape[0]* (2/3)):
                    area_list_top.append(areatop)
                    print(area_list_top)
                else:
                    area_list_top.append(0)
                    print(area_list_top)
                #print(areatop)
                cv2.drawContours(ft,[c], -1,(0,0,0),2)
                cv2.putText(ft, "Area: {}mm".format(str(areatop)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2)
        for c in cntsbottom:
            if cv2.contourArea(c) > minpixelarea:
                areabottom += cv2.contourArea(c)
                cv2.drawContours(fb,[c], -1,(0,0,0),2)
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(fb, (cx,cy),3, (255,255,255), -1)
                cv2.putText(fb, "Centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                if cy > int(fbottom.shape[0]*(1/3)) and cy < int(fbottom.shape[0]* (2/3)):
                    area_list_bottom.append(areabottom)
                    #print(area_list_bottom)
                else:
                    area_list_bottom.append(0)
                    #print(area_list_bottom)
                cv2.putText(fb, "Area: {}mm".format(str(areabottom)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2)
        #print('areatop = ',areatop)
        #print('areabottom = ',areabottom)
        vstackmask = np.vstack((masktop, maskbottom))
        vstack = np.vstack((ft,fb))
        #cv2.imshow('res',newmask)
        #print(ftop.shape)
        #cv2.imshow("Video", frame)
        cv2.imshow('masked', vstackmask)
        cv2.imshow('f', vstack)
        k = cv2.waitKey(50) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            cap.release()
    for i in range(len(area_list_top)):
        if area_list_top[i-1] == 0 and area_list_top[i] !=0:
            splitareatop.append(area_list_top[i:i+8])
    print(area_list_top)
    print(splitareatop)
    for i in range(len(splitareatop)):
        mmavg = (sum(splitareatop[i])/len(splitareatop[i]))
        avg_area_list_top.append(mmavg)
    for i in range(len(area_list_bottom)):
        if area_list_bottom[i-1] == 0 and area_list_bottom[i] !=0:
            splitareabottom.append(area_list_bottom[i:i+8])
    for i in range(len(splitareabottom)):
        mmavg = (sum(splitareabottom[i])/len(splitareabottom[i]))
        avg_area_list_bottom.append(mmavg)
    avgareatop = sum(avg_area_list_top)/len(avg_area_list_top)
    avgareabottom = sum(avg_area_list_bottom)/len(avg_area_list_bottom)
    video_dict = {
                  "average droplet area list top" : avg_area_list_top,
                  "average droplet area list bottom" : avg_area_list_bottom,
                  "average dropelt area top" : avgareatop,
                  "average droplet area bottom" : avgareabottom}
    print(video_dict)
    with open(outputfile, "w") as f:
        for key in video_dict.keys():
            f.write("%s,%s\n"%(key,video_dict[key]))
else:
    print('INVALID INPUT')
    
    