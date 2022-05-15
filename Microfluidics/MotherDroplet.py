'''
##################################################################################################################################
#                       Summary:                                                                                                 #
#        This program utlizes OpenCV, an open source python library tailored towards computer vision appplications.              #
#        This program aims to measure the area of micro and millifluidic droplets that underwent a forming or                    #
#        merging operation. In other words, a merging operation is when a millifluid droplet is merged with another              #
#        millifluidic droplet, thus created creating a larger droplet. The color boudn finder window is broken into the          #
#        frame with the droplets and the hsv slider for minimum and maxium hsv bounds. The droplet analysis interface is         #
#        broken into 3 windows. the top window, is the original cropped video with a maximum of 2 droplets per frame.            #
#        This windw calculates the distance between droplets, the diamter of a dropelt, the velocity of a droplet, area of       #   
#        a droplet, and the perimeter of a droplet.  The bottom left window just calcualtes the area and perimeter of a          #
#        droplet (the original frame just split in half. the bottom right shows the mask to ensure accurate droplet              #
#        detection.  This Program allows the user to input a cropped video of millifluid dropelts either                         #
#        forming or merging, and analyze the mother droplets area, perimeter, velocity, distance, and diameter.                  # 
#        The program has a builtin HSV control slider such that a user can accruatly detect different color                      #
#        droplets from different videos because no one video is the same.  Teh HSV manipulator allows the user                   # 
#        to define lower and upper bounds for droplet detection.  Its an iteravtive process to get good results.                 #
#        run the video to see areas that are being detected. stop the process and change the minpixelarea,                       # 
#        the minumim area you want the program to measure. run it again and you may need to change the area                      #
#        bounding lines etc to ensure the droplet is fully in the frame.  The mask will either be a positive                     #
#        or negative mask. if its negative. it will only show the droplet in the hsv manipulatar window,                         #
#        everything else is blacked out. if its positive, it ill show the dropelt blacked out. if its                            #
#        blacked out subtract 255 to lines 200 and 201. this isnt always neccesary because if you                                #
#        can syntehsise a negative mask, you can also syntehsis a positive mask using the HSV sliduers.                          # 
#                                                                                                                                #
#                       Moving Forward:                                                                                          # 
#        This program would function 10 times better if there was a data collection method that had the camera in the exact      #  
#        same place each run. this could elimates cropping of the video in an alternate software. If there was some sort of      # 
#        jig that could hold the camera above the manifold in the exact same spot everytime. Alot of the variation in            #    
#        this code could be eliminited,  especially the pixel to metric conversion, and changing the calcualtion bound           #
#        lines for when the droplets areas are caclualatd.  Also, a more accurate micron ruler could be used for                 #
#        the pixel to metric variable instead of a standard millimeter ruler. Use a better camera                                #
#                                                                                                                                #
#                                                                                                                                #
#                       Slider Tips:                                                                                             #
#        to detect the droplet, start by either sliding the hmax slider to around 70. this will usually produce a                #
#        negative mask with the droplet blacked out. the output console will update and print the upper and lower                #
#        bounds for you to monitor or record. to detect a negative mask, slide the smin slider to around 30. for                 #
#        the mother droplet code. the default mask is a posiive mask with smin around 30. if you cant get a positive             # 
#        mask, subtract 255 from the liens metnioned above.                                                                      #
#                                                                                                                                #
#                                                                                                                                #
#                                                                                                                                #
#                                                                                                                                #
#                                                                                                                                #
#                                                                                                                                #
#        press q to exit the color bound detector window and to move on to the droplet analysis window                           #
#        press esc to exit the droplet analysis window or just stop the program in kernel                                        #
#                                                                                                                                #             
#        variables to change or to ensure better results:                                                                        #   
#                    - outputfile - the file to witch you save the results to ( a .csv file)                                     #
#                    - videofile - the video file of interest (.mov or .mp4)                                                     # 
#                    - refdist - the reference distance measure from a ruler. This will be the width of                          # 
#                                the frame in mm. When you divide by the wdith of the frame in pixels,                           #  
#                                you get a scale factor to multiply all the mearued areas by.                                    #      
#                    - scalepercent -  this is the scale factor to scale the frame size by, to fit your desktop window           #   
#                    - wait - how fast the frames are analyzed                                                                   #
#                    - colorlowerbound -  the lower HSV color bound threshold for droplet detect (H,S,V). you can                #
#                                            manually change this is you already have a good upper and lower color               # 
#                                            bound for that video                                                                # 
#                    - colorupperbound - the upper ....                                                                          #      
#                    - blur - How muhc the frame is blurred. this may be changed but not neccesary (tuple)                       #
#                    - minpixelarea - this is the minimum area limit. If a the total area measured is 20000.                     # 
#                                        the min pixel area should be around 18000. This eliminates inaccurate                   # 
#                                        noise into the droplet area measurment. the ouput console will print the                #
#                                        total area that the mask has detected, thus to eliminate small areas that               # 
#                                        are not the droplet, make use of the minpixelarea                                       #
#                    - you can also rotate the frame 90 degrees on line 162 and 269                                              #
##################################################################################################################################   
'''
import cv2
import numpy as np
import imutils
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist
import csv




#these are variables user would have to change depending on the video 
file  = 'zoomrge'

outputfile = file +'.csv' # name of output csv file to write the data to
videofile = file +'.mov'

refdist = 9.3 #16.3   # size in mm of height of frame from fiducial markings

blur = (20,20) # the hgiher this is the mort blurry the image will be
scale_percent = 20 # percentage out of a hundred to scale the frame up or down

#start min pixel at 0. then run the program and observer the console ouput for measured area
minpixelarea = 19000 # the areas to exclude from area calcution if less than this number. if the areas being meaured are 20000, then min pixel area should be around 18000

flowrateoil = 500
flowratewater = 125
unitsQ = 'ul/min'
unitsM = 'mm'
################################3








#midoint function. calcualtes the midpoint given 2 points and their corodinates
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)



'''

if centroid is within yellow lines, start calculating area
if 2 droplets are in frame, calcualate distance between centroids
the diamter is measured by calcualte the midpoint of the right bounding box edge subtract from the left bounding box edge of one of the dropelts in frame


'''

cap = cv2.VideoCapture(videofile)
#cap = cv2.VideoCapture("largedropclear.MOV")
#cap.set(1,150)
totalframes = cap.get(7)
fps = cap.get(5)
duration = totalframes/fps # computes the length of the video based on how many frames are present and the fps of the video
print('This video is', round(duration,2), 'seconds long')

#minpixelarea = 30000 # change this to remove small areas that would interfere with the droplet area

# same function from DaughterDropelt code
def ColorBoundFinder():
    def nothing(x):
        pass
    #cap = cv2.VideoCapture(videofile)
    cv2.namedWindow('HSV')
    # create trackbars for color change
    cv2.createTrackbar('HMin','HSV',0,179,nothing) # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin','HSV',0,255,nothing)
    cv2.createTrackbar('VMin','HSV',0,255,nothing)
    cv2.createTrackbar('HMax','HSV',0,179,nothing)
    cv2.createTrackbar('SMax','HSV',0,255,nothing)
    cv2.createTrackbar('VMax','HSV',0,255,nothing)
    
    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'HSV', 179)
    cv2.setTrackbarPos('SMax', 'HSV', 255)
    cv2.setTrackbarPos('VMax', 'HSV', 255)
    
    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0
    cap = cv2.VideoCapture(videofile)
    #qcap.set(1,100)
    while(1):
    
        
        ret, img = cap.read() 
        img  = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)    # rotate frame
        #scale_percent = 60 # percentage out of a hundred to scale the frame up or down
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dsize = (width, height)
        img = cv2.resize(img, dsize)
        output = img
    
        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin','HSV')
        sMin = cv2.getTrackbarPos('SMin','HSV')
        vMin = cv2.getTrackbarPos('VMin','HSV')
    
        hMax = cv2.getTrackbarPos('HMax','HSV')
        sMax = cv2.getTrackbarPos('SMax','HSV')
        vMax = cv2.getTrackbarPos('VMax','HSV')
    
        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
    
        # Create HSV Image and threshold into a range.
        img = cv2.blur(img,blur)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)
    
        # Print if there is a change in HSV value
        if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            #print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax
            
            lowerbound = [hMin, sMin, vMin]
            upperbound = [hMax, sMax, vMax]
            print('Lower Bound is',lowerbound,'     ','Upper Bound is', upperbound)
            
    
        # Display output image
        cv2.imshow('HSV',output)
    
        # Wait longer to prevent freeze for videos.
        wait = 500 # 
        if cv2.waitKey(wait) & 0xFF == ord('q'): #press q to quit out of the window
            break
    cap.release()
    cv2.destroyAllWindows()
    return lowerbound, upperbound




def DropletAnalysis(bound):
    colorlowerbound = bound[0] #[10,25,25] #lower blue detection bound / change this depending on the color of the dropelt
    colorupperbound = bound[1] #[120,255,255] #upper blue detection bound
    print(colorlowerbound)
    print(colorupperbound)
    
    
  
     # the hgiher this is the mort blurry the image will be
    
    
    ay1 = 1/3
    ay2 = 2/3
    
    area_list = [] # the area of a droplet every frame, and if a droplet is not present add 0
    splitarea = [] #this splits the list above into a nest list of all the areas for 1 droplet
    avg_area_list = [] # this is the list that averages a droplet so we have an average area for each droplet in frame
    
    per_list = [] # same idea above but for the perimeter of droplet
    splitper =[]
    avg_per_list = []
    
    # same idea above but for distances between droplets
    dist_list = []
    splitdist = []
    avg_dist_list = []
    
    dia_list = []
    splitdia = []
    avg_dia_list= []
    
    # these lists are used for a velocity computation utliing the difference in frames between one droplet and the next
    framecount = []  
    finalframecount = []
    vellist = []
    
    
    EntranceCounter = 0 # not really used
    
    
    intvl = 1 # determines how the intervala t which the program reads and anlzys frames
    framelist = np.arange(0, totalframes, intvl) # an array in range from 0 to the totall number of frames in the video
    
    
    
    
    
    #begin looping through every frame
    for i in framelist:
       
        _ , frame = cap.read()
        frame  = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)                                                # rotate frame if need be
        f = frame.copy()
        cap.set(1, i)
        if frame is None:
            break
        
        
        print("                                                        ",i,'/',totalframes) #update the user which frame is being analyzed
       
        
        
        
        #resize the frames to fit in window
        #scale_percent = 60
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dsize = (width, height)
        frame = cv2.resize(frame, dsize)
        
       
        
        #copys the oringal video for mark up later
        f = frame.copy()
        #print('frame area = ', f.shape[0]*f.shape[1])
        
        fc = f[:frame.shape[1], 0:int(frame.shape[1]/2)]# new frame crop for single droplet
        
        f2 = fc.copy()
        
        # blurs the frame 
        frame = cv2.blur(frame,blur)
        fc = cv2.blur(fc, blur)
        #converts frame from blue green red to hue saturation value
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(fc, cv2.COLOR_BGR2HSV)
    
        #determine upper and lower bounds for detectiing color
        lower = np.array(colorlowerbound) #10,25,25]) lower blue
        upper = np.array(colorupperbound)#120,255,255]) upper blue
        mask = cv2.inRange(hsv, lower, upper)
        mask2 = cv2.inRange(hsv2, lower, upper)
        
        
        #m2 = mask2.copy()
        res = cv2.bitwise_and(f2,f2, mask = mask2)
        
        
      
        #start finding contours for distance iamge
        cnts =  cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cnts = imutils.grab_contours(cnts)
        (cnts, _) = contours.sort_contours(cnts)
        
        #start finding contours for single image
        cnts2 =  cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cnts2 = imutils.grab_contours(cnts2)
        (cnts, _) = contours.sort_contours(cnts)
        
    
        '''
        #counter crosing lines purple
        start = (int(f2.shape[1]/2), 0)
        end = (int(f2.shape[1]/2) , int(f2.shape[0]))
        cv2.line(f2, start, end,(255, 0, 255), 2) 
        '''
        #draws lines for area bounding lines
        cv2.line(f2, (int(f2.shape[1]*(ay1)),0),(int(f2.shape[1]*(ay1)),int(f2.shape[0])),(0, 255, 255), 2) #area exit line
        cv2.line(f2, (int(f2.shape[1]*(ay2)),0),(int(f2.shape[1]*(ay2)),int(f2.shape[0])),(0, 255, 255), 2) #area entrance line
        
       
        
        '''
        #pixel to metric refence length bounding lineslines, uses the channel width of 1 mm for conversion scale, not accurate enough
        tstart=(0,int(frame.shape[0]*(hy1)))
        tend = (int(frame.shape[1]),int(frame.shape[0]*(1/3)))
        bstart= (0,int(frame.shape[0]*(hy2)))
        bend=(int(frame.shape[1]),int(frame.shape[0]*(5.5/7)))
        cv2.line(f, tstart,tend,(0, 0, 0), 2) #top line
        cv2.line(f, bstart,bend,(0, 0, 0), 2) #bottom line
        '''
        
        #computes the distance between the top channel line and bottom channel line
        #refdist =  (bstart[1] - tstart[1])
        #refdist stuff
        
        
        
        #only need this if using fiducials
        #change to widht for fidicuals (ruler width) since wont be able to mark across the channel
        pixeldist = frame.shape[1]
        scale = refdist/pixeldist # mulitply any measurment in pixels by this scale number
          
        
        
        
        area = 0
        refObj = None
        
        #color for bounding boxe of left and right droplet
        secondcirclecolor = (10,255,0)
        firstcirclecolor = (255,255,0)
        
        area2 = 0
        perimeter = 0
        
        
        # this section pertains the the single droplet analysis of area, permeter etc
        #start looping through contours
        
        for c in cnts2:
            if (cv2.contourArea(c) > minpixelarea):# and (cv2.contourArea(c) < minpixelarea*3): # if the measured droplet area is greater than the min pixel area defined above and its less then twice minpixelarea, add that area to a list
                perimeter += cv2.arcLength(c,True) # same as above but instead add perimter
               
                area2 += cv2.contourArea(c) # add the area to the lost
                cv2.drawContours(f2,[c], -1,(0,0,0),2) # draw the contours for a visual aid for dropelt detection accuracy
        print("area2 = ", area2) # print the area of the bottom left window, calcualting droplet area
        print("min pixel area = ", minpixelarea) #min pixel area, should be alittle less than area2 above, change in beginning of code after running once
        #print(perimeter*scale)
        
        
        if (area2 > minpixelarea):# and (area2 < minpixelarea*1.5): # if the area is greater than min pixel area defined above, calcuatle the centroid from image moments
            M = cv2.moments(mask2)
            if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(f2, (cx,cy),3, (255,255,255), -1) # put a circle at the centroids coordinates
                cv2.putText(f2, "Centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1) #label the centroid
                
                
                
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int") 
                box = perspective.order_points(box)
                
                objCoords = np.vstack([box, (cx, cy)])
                
                
                (srx,sry) = midpoint((objCoords[1][0],objCoords[1][1]),(objCoords[2][0],objCoords[2][1])) # the midpoint of the right droplets right edge
                (slx,sly) = midpoint((objCoords[3][0],objCoords[3][1]),(objCoords[0][0],objCoords[0][1]))# midpoint of the right dropelts left edge
                #draw a circl at those midpoint edges for observation, uncomment if you want to double check the lcoaiton
                #cv2.circle(ft, (int(srx),int(sry)),9, (255,255,255), -1)
                #cv2.circle(ft, (int(slx),int(sly)),9, (255,255,255), -1)
                
                #thus the lengthwise diameter is the the midpoint of the top edge subtracted by the midpoint of the bottom edge
                diameter = srx - slx
                #print(diameter*scale)
                
                cv2.line(f2, (int(srx), int(sry)), (int(slx), int(sly)),(0, 0, 255), 2)  # draw red diamter line
            
            
            
            
            #print(cx,cy)
            
            else:
                center = (0,0) 
            
            
            #below was an attempt for counting droplets. but then realized if I know the areas of each droplet (that were appended to a list) then the length of that list is the number of droplets
            # the idea was that if the centroid was near a certain line, add 1 to a counter. thi didnt work because seomtimes to cetroid would appear near the line more than once, thus counting 1 droplet twice.
            absdistance = abs(cx-f2.shape[1]/2)
            #print(absdistance)
         
            if (absdistance <= 20):
                framecount.append(int(i))
                EntranceCounter +=1
                #print(framecount)
            
            
        
            if cx < int(f2.shape[1]*(ay2)) and cx > int(f2.shape[1]* (ay1)): # if the cenroid of the droplet is within specified yellow bounding lines. add the area to a list. This allows teh dropelt area to be cacluated numerous times while it is within these lines, and then averaged to get an avergae area for tht dropelt. more accurate
                per_list.append(perimeter) # if its within these lines append the perimeter and area to a list
                area_list.append(area2)
                dia_list.append(diameter)
                
                cv2.putText(f2, "Area: {}mm".format(str(area2*(scale**2))), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2) #label the area and perimter to keep the user up to date and observce discrepencies 
                cv2.putText(f2, "Perimeter: {}mm".format(str(perimeter*(scale))), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2)
                cv2.putText(f2, "Dia:{}mm".format(str(diameter*(scale))), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 1), 2)
                #print(area_list)
                #print(per_list)
            # if the cetroid is not within these bounding lines add 0 to this same list. these 0s act as spacers to allow us to split the list at these zeros to get an indivudal average single dropelt area
            else:
                area_list.append(0)
                per_list.append(0)
                dia_list.append(0)
                #print(area_list)
                #print(per_list)
                
           
           
                
                
                
               
        # this section pertains to the distance calculation 
                
        for c in cnts:
            if (cv2.contourArea(c) > minpixelarea):# and (cv2.contourArea(c) < minpixelarea * 2): # same idea above
               
                area += cv2.contourArea(c)
                cv2.drawContours(f,[c], -1,(0,0,0),2)
                
                # this time draw a box around the left most dropelt
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int") 
                box = perspective.order_points(box)
        	
           
        # compute the center of the bounding box
         #finds center of bounding box by taking average of boundbox in both x and y direction
                cX = int(np.average(box[:, 0]))  #another way of finding the centroid, finds teh center of the bounding box
                cY = int(np.average(box[:, 1]))
                
                #create a reference object to meaure the distance from this droplet to the next
                if refObj is None:
                    (tl, tr, br, bl) = box
                    (tlblX, tlblY) = midpoint(tl, bl) #midpoint of right edge of bounding box of left most droplet
                    (trbrX, trbrY) = midpoint(tr, br)  #midpoint of left edge of bounding box of left most droplet
                    D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                    refObj = (box, (cX,cY), D) # add D/width of left most obect in real life (inches) # not neccesary
                  # reference object is 3 tuple of(sorted coords, centroid of reference object, pixels per metric ratio)
                    
                    continue
                
                cv2.drawContours(f,[box.astype('int')], 0, secondcirclecolor,2) #(10,255,0) = neon green #draws the contours on the origanl image frame in neon green of the left most dropelt
                cv2.drawContours(f, [refObj[0].astype("int")], -1, firstcirclecolor, 2) # draws the contours on the right most droplet
                refCoords = np.vstack([refObj[0], refObj[1]])
                objCoords = np.vstack([box, (cX, cY)])
                #first and second cicles centroids (circle implies droplet, to lazy to change, even tho there is a built in replace function in spyder)
                firstcircleX = refCoords[4][0]
                firstcircleY = refCoords[4][1]
                secondcircleX = objCoords[4][0]
                secondcircleY = objCoords[4][1]
                
               
                
               
                (srx,sry) = midpoint((objCoords[1][0],objCoords[1][1]),(objCoords[2][0],objCoords[2][1])) # the midpoint of the right droplets right side bounding box edge
                
                #thus the lengthwise diameter is the the midpoint of the left edge subtracted by the midpoint of the right edge
                
                
                
                if trbrX > int(frame.shape[1]*0) and srx < int(frame.shape[1]*(19/20)): # if the left droplets right edge is greater than the left edge of the frame, and the right droplets right edge is less than the right edge of the frame, start finding the distance between the droplets
                    
                    cv2.circle(f, (int(trbrX),int(trbrY)),9, (0,0,0), -1) 
                    cv2.circle(f, (int(srx),int(sry)),9, (0,0,0), -1) 
                    
                 
                        
                    #print(dia_list)
        
                   
                    
                    #euclidean distance btween the left dropelt and right droplet
                    D = dist.euclidean((trbrX, trbrY), (srx, sry)) 
                    
                    (mX, mY) = midpoint((trbrX, trbrY), (srx, sry))    
                    cv2.putText(f, "{:.1f}mm".format(D*scale), (int(mX), int(mY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,0), 2)   
                    
                    cv2.circle(f, (cX,cY),3, (255,255,255), -1)
                    
                    cv2.putText(f, "Centroid", (cX-20,cY-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                    cv2.circle(f, (int(firstcircleX),int(firstcircleY)),4, firstcirclecolor, -1) #draws midpoint of right edge of bounding box
                    cv2.circle(f, (int(secondcircleX),int(secondcircleY)),4, secondcirclecolor, -1) #draws midpoint of right edge of bounding box 
                    cv2.line(f, (int(trbrX), int(trbrY)), (int(srx), int(sry)),(0, 0, 255), 2) 
                    dist_list.append(D)
                    
        #print("area = ", area) # print the area of the top window, the window with 2 droplets calcualating distance/diameter. so the minpixel area should be around twice as less as the top window area since there are 2 droplets
        
        #if the top total droplet area is less than 1.5 droplets add zero. this ensures we are not finding distances if there are less than 2 droplets in the frame
        if area < minpixelarea*1.5:
            dist_list.append(0)
            
            
            
       
                    
               
                
        
        

        # arange the frames in a nice way for the user
        
        #an error may occur saying theat the input arrarys must match.  this means the numpy_h is not the same size as the orignal frame f. just comment out   numpy_h and uncomment the seocnd cv2.imshow line 
        
        numpy_h = np.hstack((f2, res))  #combines the single droplet frame and its respective mask into one window
        numpy_v = np.vstack((f, numpy_h)) # combines the above window with the double droplet window
        
        
        #cv2.imshow('im', f) 
        cv2.imshow('im3', numpy_v)
        
        
        
        wait = 20
        k = cv2.waitKey(wait) & 0xFF  # press escape to exit the window
        if k == 27:
            cv2.destroyAllWindows()
        
            cap.release()
    
    #averae distance loops and lists, add the first 4 indexs of the list to avoid avershooting the list and adding zeros
    for i in range(len(dist_list)):
        if dist_list[i-1] == 0 and dist_list[i] !=0:
           splitdist.append(dist_list[i:i+5])
    
    for i in range(len(splitdist)):
        mmavg = (sum(splitdist[i])/len(splitdist[i]))*scale
        avg_dist_list.append(round(mmavg,2))
        
        
        
        
        
    #average diameter loops and lists
    for i in range(len(dia_list)):
        if dia_list[i-1] == 0 and dia_list[i] !=0:
           splitdia.append(dia_list[i:i+5])
    
    for i in range(len(splitdia)):
         mmavg = (sum(splitdia[i])/len(splitdia[i]))*scale
         avg_dia_list.append(round(mmavg,2))
    
   
    
   
    
    #average area loops and lists
    for i in range(len(area_list)):
        if area_list[i-1] == 0 and area_list[i] !=0:
            splitarea.append(area_list[i:i+5])
    
    for i in range(len(splitarea)):
        mmavg = (sum(splitarea[i])/len(splitarea[i]))*(scale**2)
        avg_area_list.append(round(mmavg, 2))
    
    
    
    
    
    #average perimeter loops and lists
    
    for i in range(len(per_list)):
        if per_list[i-1] == 0 and per_list[i] !=0:
            splitper.append(per_list[i:i+5])
    
    for i in range(len(splitper)):
        mmavg = (sum(splitper[i])/len(splitper[i]))*(scale)
        avg_per_list.append(round(mmavg, 2))
    
    #distance
    avgdist = sum(avg_dist_list)/len(avg_dist_list)
    #area
    avgarea = sum(avg_area_list)/len(avg_area_list)
    #perimeter
    avgper = sum(avg_per_list)/len(avg_per_list)
    #diamter
    avgdia = sum(avg_dia_list)/len(avg_dia_list)
    
    
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
    
    
    
    
    
    #DISPLAY RESULTS
    #print("average number of frames between each droplet = ", avgframe, 'frames')
    
    print('======PERIMETER STATS======')
    #print("perimeter of each droplet = ", avg_per_list)
    print("average perimeter of droplet = ", round(avgper,2), 'mm\n')
    
    
    
    print('======VELOCITY STATS======')
    #print("velocity of each droplet = ", vellist)
    print("average velocity of droplet = ", round(avgvel,2), 'mm/s\n')
    
    
        
    print('======DISTANCE STATS=======')
    #print('average distance between droplets list = ', avg_dist_list)
    print('average distance between droplets  = ', round(avgdist, 2), 'mm\n')
    
    print('======DIAMETER STATS=======')
    #print('average lengthwise diameter between droplets list = ', avg_dia_list)
    print('average diameter between droplets  = ', round(avgdia, 2), 'mm\n')
    
    
    print('======AREA STATS========')
    #print('average dropelt area list = \n', avg_area_list)
    print('average droplet area = ', round(avgarea, 2), 'mm^2\n')
    
    print('=======COUNTING STATS=======')
    #print('# areas measured = ', len(avg_area_list))
    print('# of droplet detected from counter = ', EntranceCounter) 
    print('# distances measured =', len(avg_dist_list))
    print('number of droplets from frame count/velocity = ', len(finalframecount)) 
    
    
    
    
    
    
    
    video_dict = {"Senior Design Project": "Mother Droplet",
                  "velocity of each droplet list" : vellist,
                  "average droplet area list" : avg_area_list,
                  "average distance between droplets list" : avg_dist_list,
                  "average droplet perimeter list" : avg_per_list,
                  "average diameter list" : avg_dia_list,
                  "Flow rate oil" : flowrateoil,
                  "Flow rate water" :flowratewater,
                  "units flow rate" : unitsQ,
                  "units metric" : unitsM
        }
       
    #print(video_dict)
    print("Flow rate oil" , flowrateoil)
    print("Flow rate water" ,flowratewater)
    print("units flow rate" , unitsQ)
    print("units metric" , unitsM)
    with open(outputfile, "w") as f:
        for key in video_dict.keys():
            f.write("%s,%s\n"%(key,video_dict[key]))


#the colorboundfinder() function returns the upper and lower bounds that you defined using the hsv sliders. then the dropeltanalysis() function reads those values to perform the analysis

DropletAnalysis(ColorBoundFinder())

cv2.destroyAllWindows()
        
cap.release()
