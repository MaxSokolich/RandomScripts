'''
###############################################################################################################################
#                       Summary:                                                                                              #
#        This program utlizes OpenCV, an open source python library tailored towards computer vision appplications.           #
#        This program aims to measure the area of micro and millifluidic droplets that underwent a splitting operation.       #
#        In other words, a splitting operation is when a millifluid droplet is propelled towards a bifurcation point,         #
#        thus splitting the droplet in half. One half of the droplet is sent down one channel and the other is sent           #
#        down a different channel, hence daughter droplets. This Program allows the user to input a cropped video of          #
#        millifluid dropelts splitting, and analyze the daugher droplets area's in order to compare how equal they. '         #
#        The program has a builtin HSV control slider such that a user can accruatly detect different color droplets          # 
#        from different videos because no one video is the same.  Its an iteravtive process to get good results. run          # 
#        the video see areas that are being detected. stop teh process change the minpixelarea. run it again and you          # 
#        may need to change the area bounding lines etc. The mask will other be a positive or negative mask. if its           #
#        negative. it will only show the droplet in the hsv manipulatar window. if its positive, it ill show the dropelt      # 
#        blacked out. if its blacked out subtract 255 to lines 252 and 271                                                    #
#                                                                                                                             #  
#                        Moving Forward:                                                                                      #
#        This program would function 10 times better if there was a data collection method that had the camera in the         #
#        exact same place each run.  If there was some sort of jig that could hold the camera above the manifold in the       # 
#        exact same spot everytime. Alot of the variation in this code could be eliminited, especially the pixel to metric    #
#        conversion, and changing the calcualtion bounds for when the droplets areas are caclualatd.  Also, a more accurate   #
#        micron ruler could be used for the pixel to metric variable.                                                         #              
#                                                                                                                             # 
#                                                                                                                             #  
#                       Slider Tips:                                                                                          #  
#        to detect the droplet, start by either sliding the hmax slider to around 70. this will usually produce a positive    #
#        mask with the droplet blacked out. to detect a negative mask, slide the smin slider to around 30. for the daughter   #
#        droplet code. the default mask is a postive mask with hmax around 70. if you cant get a negative mask, remove        #
#        the (subtract 255) from the lines metnioned above.                                                                   #
#                                                                                                                             #      
#                                                                                                                             #      
#                                                                                                                             #      
#                                                                                                                             #      
#                                                                                                                             #      
#                                                                                                                             #      
#        press q to exit the color bound detector window and to move on to the droplet analysis window                        #
#        press esc to exit the droplet analysis window                                                                        #
#                                                                                                                             #       
#        paribles to change or to ensure better results:                                                                      #
#                    - outputfile - the file to witch you save the results to ( a .csv file)                                  #
#                    - videofile - the video file of interest (.mov or .mp4)                                                  #  
#                    - refdist - the reference distance measure from a ruler. This will be the width fo the frame in mm.      #
#                                    and when you divide by the wdith of the frame in pixels. you get a scale factor to       #
#                                    multiply all the mearued areas by.                                                       #  
#                    - scalepercent -  this is the scale factor to scale the frame size by, to fit your desktop window        #
#                    - wait - how fast the frames are analyzed                                                                #
#                    - colorlowerbound -  the lower HSV color bound threshold for droplet detect (H,S,V)                      #
#                    - colorupperbound - the upper ....                                                                       #  
#                    - blur - How muhc the frame is blurred. this may be changed but not neccesary (tuple)                    #
#                    - minpixelarea - this is the minimum area limit. If a the total area measured is 20000.                  #
#                                    the min pixel area should be 18000. This eliminates inaccurate noise into the droplet    #  
#                                    area measurment                                                                          #
#                    - you can also rotate the frame 90 degrees on line 123 and 222                                           #
###############################################################################################################################
'''



import cv2  # opencv library
import numpy as np # number python library
import imutils # image utilities libarary
from imutils import perspective
from imutils import contours
import csv #comma separated values library

#midoint function. calcualtes the midpoint given 2 points and their corodinates
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


'''
##########################################################################################################################################################################################
'''

# paaremeters to change below
refdist = 2.7               # mm  ,   the distance measure from the ruler, after finialized, cropped video

#these are variables user would have to change depending on the video 
file  = '11-10-20-T1'

outputfile = file +'.csv' # name of output csv file to write the data to
videofile = file +'.mov'


blur = (20,20) # the hgiher this is the mort blurry the image will be
scale_percent = 100 # percentage out of a hundred to scale the frame up or down
minpixelarea = 0 #  exclude pixel areas that are less than 2000. if the droplet area is 20000 pixels, the minpixelarea should be around 17000 pixels


flowrateoil = 400               # the flow rate of oil inputed to pump
flowratewater = 100             # the flow rate inputed of water to pump
unitsQ = "ul/min"               # units for flowrate
unitsM = "mm"                   # units of measurements

# these are the y positions of the bounding lines for the top droplet frame and the bottom droplet frame respecitvly 
 # change these if applicaible to make sure the entire droplet is in frame and areas are calcualted for the full dropelt. droplet is not cutoff. these lines may need to be changed whether or not you are analyzing a Y junction splitting video or a T junction splitting video.
toplinet =  2/5  #top line (distance from top of frame) for the top droplets
bottomlinet = 3/5 #bottom line (distance from top of frame)for the top dropelts
toplineb =  2/5  #top line (distance from top of frame) for the bottom droplets
bottomlineb = 3/5 #bottom line (distance from top of frame) for the bottom droplets

'''
###################################################################################################################################################################3########3######################################################
'''

cap = cv2.VideoCapture(videofile)      #capture video file object




totalframes = cap.get(7)
fps = cap.get(5)
duration = totalframes/fps # computes the length of the video based on how many frames are present and the fps of the video
print('This video is', round(duration,2), 'seconds long')


def ColorBoundFinder():
    '''
    This function allows the user to determine the upper and lower 
    hue saturation value bounds for droplet detection. 
    Mainly change the maximumm hue slider for detecton
    
    ouputs color bounds used in DropletAnlaysis function 
    
    '''
    
    def nothing(x):
        pass
    
    cv2.namedWindow('HSV')                          #create window to store sliders and video frames
    
    # create trackbars for color change
    cv2.createTrackbar('HMin','HSV',0,179,nothing)  # Hue is from 0-179 for Opencv
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
    
    #begin looping through frames
    while(1):
    
       
        
        ret, img = cap.read()                                   #begin reading video file
        img  = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)         #comment or uncomment to rotate frame 90 degrees clockwise when applicble 
        # percentage value to scale the frame in order to fit on desktop res
        width = int(img.shape[1] * scale_percent / 100)         # rescale the width of the video frame using scale value
        height = int(img.shape[0] * scale_percent / 100)        # rescale the height of the video frame using scale value
        dsize = (width, height)                                 
        img = cv2.resize(img, dsize)                            # resize original frames size using width and height values above
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
        img = cv2.blur(img, blur)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)
    
        # Print if there is a change in HSV value
        if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax
            
            lowerbound = [hMin, sMin, vMin]                                         # lower bound to be output to Droplet Analysis function below
            upperbound = [hMax, sMax, vMax]                                         # upper bound to be output to Dropelt Analysis function below
            print('Lower Bound is',lowerbound,'     ','Upper Bound is', upperbound) # prints the upper and lower color bounds everytime the slider is changed
                                                                                    # record the adequate detection these values if you need to alter the code for the same video
    
        
        
        cv2.imshow('HSV',output)                     # display video , (replace output with mask if you want to see a binary image)
    
        wait = 1000                                  # decrease this number if you want the video to go faster and vice versa
        
        if cv2.waitKey(wait) & 0xFF == ord('q'):     # press q to quit out of the window once adequate detection bounds are found ( change )
            break
    cap.release() # release the video 
    cv2.destroyAllWindows() # quit the window if the "g" key is pressed, and move onto to the DropletAnaysis function
    
    return lowerbound, upperbound 


def DropletAnalysis(bound):
    '''
    
    This function analyzes the droplets area. It utilizes 2 bounding lines to tell the program 
    to start appending data if the centroid of the droplet is within these lines. 
    this prevents unwanted area calculations if the droplet is not fully in frame.
    
    inputs the color bound tuple from ColorBound Finder Above
    
    outputs a average area for both top and bottom droplets, and writes all areas of each droplet to a csv
    
    '''
    colorlowerbound = bound[0] # lower color bound (H,S,V) # change this if you already recorded an accurate lowerbound
    colorupperbound = bound[1] # upper color bound (H,S,V) # cange this if you alredy recorded an accurate upperbound
    
    
    
    lower = np.array(colorlowerbound) 
    upper = np.array(colorupperbound)
    
    #top droplet area list orgainzation
    area_list_top = [] #this calcualtes the area of a droplet every frame if its within bounding lines, and if a droplet is not present add 0
    splitareatop = [] #this splits the list above into a nest list if a 0 is present. this allows us to isolate a droplet from the next
    avg_area_list_top = [] #this then averages the values in the nested list above, to get an average single droplet area for that frame
    
    #same as above but for bottom dropelts
    area_list_bottom = [] 
    splitareabottom = [] 
    avg_area_list_bottom = [] 
    
    
    
    dia_listT = []
    splitdiaT = []
    avg_dia_listT= []
    
    
    dia_listB = []
    splitdiaB = []
    avg_dia_listB = []
    
   
    
   # change these if applicaible to make sure the entire droplet is in frame and areas are calcualted for the full dropelt
    

    intvl = 1 # determines how the intervala t which the program reads and anlzys frames
    framelist = np.arange(0, totalframes, intvl) # an array in range from 0 to the totall number of frames in the video





    for i in framelist:
        ret, frame = cap.read() 
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cap.set(1, i)
        if frame is None: # if the frame reads none, stop looping through frames and terminate the program
            break
        
        print("                                                        ",i,'/',totalframes) #update the user which frame is being analyzed
        #######################################################################################################
        
        #print(frame.shape)
        
        
        #same resize block from above function to resize image
        ftop = frame[0:int(frame.shape[0]*(1/2)),:frame.shape[1]] # split the frame in half. Top half will have the top droplets
        widtht = int(ftop.shape[1] * scale_percent / 100)
        heightt = int(ftop.shape[0] * scale_percent / 100)
        dsizet = (widtht, heightt)
        ftop = cv2.resize(ftop, dsizet)
        
        ft = ftop.copy() # copy the image so the original image can be used later
        
        # top and bottom bounding lines for area additions
        cv2.line(ft, (0,int(ftop.shape[0]*(bottomlinet))),(int(ftop.shape[1]),int(ftop.shape[0]*(bottomlinet))),(0, 255, 255), 2) #area exit line
        cv2.line(ft, (0,int(ftop.shape[0]*(toplinet))),(int(ftop.shape[1]),int(ftop.shape[0]*(toplinet))),(0, 255, 255), 2) 
        
        ftop = cv2.blur(ftop, blur)    #blur the image so that the droplet can be detected easier than with a grainy mask (may change this if see fit)
        hsvtop = cv2.cvtColor(ftop, cv2.COLOR_BGR2HSV) #convert original image frame to HSV 
        # blacked out mask here subtract 255 below
        masktop = 255 - cv2.inRange(hsvtop, lower, upper) # apply the mask using upper and lower color bounds from last function (255-, part is to invert the mask so black is white or white is black depending on whats easier)
        
        #begin finding and grabbing contours based on the edges of the mask
        cntstop =  cv2.findContours(masktop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cntstop = imutils.grab_contours(cntstop)
        
        #######################################################################################################
        
        # same idea for above analysis but for bottom half of frame (bottom droplets)
        fbottom = frame[int(frame.shape[0])- int(frame.shape[0]/2):, :frame.shape[1]] # split the frame in half. Bottom half will have the bottom dropelts
        widthb = int(fbottom.shape[1] * scale_percent / 100)
        heightb = int(fbottom.shape[0] * scale_percent / 100)
        dsizeb = (widthb, heightb)
        fbottom = cv2.resize(fbottom, dsizeb)
        fb = fbottom.copy()
        cv2.line(fb, (0,int(fbottom.shape[0]*(toplineb))),(int(fbottom.shape[1]),int(fbottom.shape[0]*(toplineb))),(0, 255, 255), 2) # bottom half can be thought of as inverted hence switching the lines 
        cv2.line(fb, (0,int(fbottom.shape[0]*(bottomlineb))),(int(fbottom.shape[1]),int(fbottom.shape[0]*(bottomlineb))),(0, 255, 255), 2) 
        fbottom = cv2.blur(fbottom, blur)
        hsvbottom = cv2.cvtColor(fbottom, cv2.COLOR_BGR2HSV)
        maskbottom = 255 - cv2.inRange(hsvbottom, lower, upper)
        cntsbottom =  cv2.findContours(maskbottom, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        cntsbottom = imutils.grab_contours(cntsbottom)
        
        
        
        
        
        #res = cv2.bitwise_and(ftop,ftop, mask = 255 - masktop)
        #framearea = ftop.shape[0] *ftop.shape[1]
        
        areatop = 0  # areas measured in pixels for top dropelts
        areabottom = 0 # areas measured in pixels for bottom droplets
        
        #print(fbottom.shape)
        pixeldist = fbottom.shape[1]  # this equals the width of the frame in pixels. Using this to create a pixel2metric conversion from ref dist ruler value in beginning
        scale = refdist/pixeldist # scale value. mulitply any measurement by this number to convert pixels to mm
        
        #start looping through contours to form a closed perimeter to find the area under
        for c in cntstop:
            if (cv2.contourArea(c) > minpixelarea):# and (cv2.contourArea(c) < minpixelarea*3): # if the contour area is greater than a certain pixel number, start finding areas. this eliminates unwanted contour noise  
                
    
                areatop += cv2.contourArea(c) # add the areas to areatop for each frame
                print("area = ", areatop)
                print("min pixel area = ", minpixelarea)
                
                M = cv2.moments(c) # iamge moments used to find the centroid
                #if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"]) # x component in pixels of droplet centroid
                cy = int(M["m01"] / M["m00"]) # y componenet in pixels of droplet centroid
                cv2.circle(ft, (cx,cy),3, (255,255,255), -1) # draw a circle at the centroid for viewer to see
                cv2.putText(ft, "Centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1) # put a text bar telling the user this dot is the centroid
                
                
                
                
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int") 
                box = perspective.order_points(box)
                
                objCoords = np.vstack([box, (cx, cy)])
                
                
                
                (srx,sry) = midpoint((objCoords[0][0],objCoords[0][1]),(objCoords[1][0],objCoords[1][1])) # the midpoint of the top edge of droplet bounding box 
                (slx,sly) = midpoint((objCoords[2][0],objCoords[2][1]),(objCoords[3][0],objCoords[3][1]))# midpoint of the bottom edge of droplet bounding box
                #draw a circl at those midpoint edges for observation, uncomment if you want to double check the lcoaiton
                #cv2.circle(ft, (int(srx),int(sry)),9, (255,255,255), -1)
                #cv2.circle(ft, (int(slx),int(sly)),9, (255,255,255), -1)
                
                #thus the lengthwise diameter is the the midpoint of the top edge subtracted by the midpoint of the bottom edge
                diametert = sly - sry
                print(diametert*scale)
                
                
                cv2.line(ft, (int(srx), int(sry)), (int(slx), int(sly)),(0, 0, 255), 2) #draw red diameter line
                
                
                
                # only add the areatop number above if the y component of the centroid is greater than the top line and less than the bottom line. ((0,0) is the top left corner of the frame, increasing moving to the right and down)
                if cy > int(ftop.shape[0]*(toplinet)) and cy < int(ftop.shape[0]* (bottomlinet)):
                    area_list_top.append(areatop*(scale**2)) # append the areatop of that frame to a list and apply scale factor to convert to mm
                    dia_listT.append(diametert*scale)
                    
                    
                    #print(area_list_top)
                    
                else:
                    area_list_top.append(0)# if the centroid is not within the bounding line,  add 0 
                    dia_listT.append(0)# if the centroid is not within the bounding line,  add 0 
                    
                    #print(area_list_top)
               
                dia = round(diametert*(scale),2)
                #print(areatop)
                cv2.drawContours(ft,[c], -1,(0,0,0),2) # draw the contours onto the image 
                cv2.putText(ft, "Area:{}mm".format(str(round(areatop*(scale**2),2))), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 1), 2) #display the all areas whether they are within bounds or not
                cv2.putText(ft, "Dia:{}mm".format(str(round(diametert*(scale),2))), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 1), 2)
        
        
        # same comments and process from above but for bottom half of image/ bottom dropelts
        for c in cntsbottom:
            if (cv2.contourArea(c) > minpixelarea):# and (cv2.contourArea(c) < minpixelarea*3):
    
                areabottom += cv2.contourArea(c)
                cv2.drawContours(fb,[c], -1,(0,0,0),2)
    
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(fb, (cx,cy),3, (255,255,255), -1)
                cv2.putText(fb, "Centroid", (cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                
           
                
                # draw a bounding box around droplet, calcualte the midpoiint of the top and bottom edge and measure distance between them to find the lengthwise diamter
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int") 
                box = perspective.order_points(box)
                
                objCoords = np.vstack([box, (cx, cy)])
                
                
                (srx,sry) = midpoint((objCoords[0][0],objCoords[0][1]),(objCoords[1][0],objCoords[1][1])) # the midpoint of the top edge of droplet bounding box 
                (slx,sly) = midpoint((objCoords[2][0],objCoords[2][1]),(objCoords[3][0],objCoords[3][1]))# midpoint of the bottom edge of droplet bounding box
                #draw a circl at those midpoint edges for observation, uncomment if you want to double check the lcoaiton
                #cv2.circle(ft, (int(srx),int(sry)),9, (255,255,255), -1)
                #cv2.circle(ft, (int(slx),int(sly)),9, (255,255,255), -1)
                
                #thus the lengthwise diameter is the the midpoint of the top edge subtracted by the midpoint of the bottom edge
                diameterb = sly - sry
                print(diameterb*scale)
                
                cv2.line(fb, (int(srx), int(sry)), (int(slx), int(sly)),(0, 0, 255), 2)  # draw red diamter line
                
                
                
                
                
                if cy > int(fbottom.shape[0]*(toplineb)) and cy < int(fbottom.shape[0]* (bottomlineb)):
                    area_list_bottom.append(areabottom*(scale**2))
                    dia_listB.append(diameterb*scale)
                    
                    #print(area_list_bottom)
                
                else:
                    area_list_bottom.append(0)
                    dia_listB.append(0)
                    #print(area_list_bottom)
                
                cv2.putText(fb, "Area:{}mm".format(str(round(areabottom*(scale**2),2))), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 1), 2)
                cv2.putText(fb, "Dia:{}mm".format(str(round(diameterb*(scale),2))), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 1), 2)
        #print('areatop = ',areatop)
        #print('areabottom = ',areabottom)
        
        vstackmask = np.vstack((masktop, maskbottom)) # re combine the top half of the masked image with the bottom half of image (not neccesary just looks cooler)
        vstack = np.vstack((ft,fb)) # recombine original image like above (not masked version)
      
        
        #cv2.imshow('res',newmask)
        #print(ftop.shape)
      
        #cv2.imshow("Video", frame)
        
        cv2.imshow('masked', vstackmask)
        cv2.imshow('f', vstack)
        
        
         
        wait = 100 # change this depending on how u want the video to go
        k = cv2.waitKey(wait) & 0xFF # assign a varible to the keyboard key "escape"
        if k == 27: #if escape is pressed terminate the program
            cv2.destroyAllWindows() 
        
            cap.release()
            
    #loop through the area list with areas and 0s. if the index is 0 and the the index afterwards is not zero, split the list into another list. Take the first 3 non xero values from that list once a zero is detected. i dont know how to tell it to take all the values in between the zeros.
    for i in range(len(area_list_top)):
        if area_list_top[i-1] == 0 and area_list_top[i] !=0:
            splitareatop.append(area_list_top[i:i+3])
   
    # loop through the new list with nested list of areas a droplet was within bounds. average those nested lists to get an average area for that one dropelt
    for i in range(len(splitareatop)):
        mmavg = (sum(splitareatop[i])/len(splitareatop[i]))
        avg_area_list_top.append(round(mmavg,2))
    
    
    #same comments as above but for bottom droplet list
    for i in range(len(area_list_bottom)):
        if area_list_bottom[i-1] == 0 and area_list_bottom[i] !=0:
            splitareabottom.append(area_list_bottom[i:i+3])
    
    for i in range(len(splitareabottom)):
        mmavg = (sum(splitareabottom[i])/len(splitareabottom[i]))
        avg_area_list_bottom.append(round(mmavg,2))
        
    # get an average area for all the top and bottom droplets in the video, 
    avgareatop = sum(avg_area_list_top)/len(avg_area_list_top)
    avgareabottom = sum(avg_area_list_bottom)/len(avg_area_list_bottom)
    
    
    #######################
    #Diamter calcualtions
    
    for i in range(len(dia_listT)):
        if dia_listT[i-1] == 0 and dia_listT[i] !=0:
           splitdiaT.append(dia_listT[i:i+4])
    
    for i in range(len(splitdiaT)):
         mmavg = (sum(splitdiaT[i])/len(splitdiaT[i]))
         avg_dia_listT.append(round(mmavg,2))
         
         
         
    for i in range(len(dia_listB)):
        if dia_listB[i-1] == 0 and dia_listB[i] !=0:
           splitdiaB.append(dia_listB[i:i+4])
    
    for i in range(len(splitdiaB)):
         mmavg = (sum(splitdiaB[i])/len(splitdiaB[i]))
         avg_dia_listB.append(round(mmavg,2))
    
    
    # get an average area for all the top and bottom droplets in the video, 
    avgdiatop = sum(avg_dia_listT)/len(avg_dia_listT)
    avgdiabottom = sum(avg_dia_listB)/len(avg_dia_listB)
   
    
   #DISPLAY RESULTS
    
    video_dict = {
                  "average droplet area list top" : avg_area_list_top,
                  "average droplet area list bottom" : avg_area_list_bottom,
                  "average droplet diameter list top" : avg_dia_listT,
                  "average droplet diameter list bottom" : avg_dia_listB
                  
                  }
  
                  
    print("average droplet diameter bottom" , avgdiatop)
    print("average droplet diameter top" , avgdiabottom)
    print("average dropelt area top" , avgareatop)
    print("average droplet area bottom" , avgareabottom)
    print("Flow rate oil" , flowrateoil)
    print("Flow rate water" ,flowratewater)
    print("units flow rate" , unitsQ)
    print("units metric" , unitsM)
    
    # write dictionary to a csv file for later analysis in excel
    with open(outputfile, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(video_dict.keys())
        writer.writerows(zip(*video_dict.values()))
        
                  
#the colorboundfinder() function returns the upper and lower bounds that you defined using the hsv sliders. then the dropeltanalysis() function reads those values to perform the analysis


DropletAnalysis(ColorBoundFinder())        

cv2.destroyAllWindows()
        
cap.release()



