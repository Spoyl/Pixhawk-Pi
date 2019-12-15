# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 19:26:10 2019

@author: Oliver
"""

import cv2
import numpy as np

IMAGE_DIR = "C:\\Users\\Oliver\\Desktop\\DroneVisionSystem\\Drone Gopro Pictures\\"
IMAGE_NAME = "G0059124.JPG"     #3648x2736
SCALE_PERCENT = 20
AREA_ARRAY = []

print("\nImage:")
print(IMAGE_DIR+IMAGE_NAME)

img=cv2.imread(IMAGE_DIR+IMAGE_NAME, cv2.IMREAD_COLOR)  # load image

# Resize
WIDTH = int(img.shape[1]*SCALE_PERCENT/100)
HEIGHT = int(img.shape[0]*SCALE_PERCENT/100)
DIM = (WIDTH,HEIGHT) 
resized = cv2.resize(img, DIM, interpolation = cv2.INTER_AREA) 

# Show stats
print("\nImage Size:\t"+str(img.shape))
print("\nResized Image:\t"+str(resized.shape))

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)    #convert to grayscale
cv2.imshow("grayscale image", gray)
cv2.imwrite("orig.jpg", gray)

ret, thresh1 = cv2.threshold(gray,210,255,cv2.THRESH_BINARY)    #threshold
#cv2.imshow("thresholded image", thresh1)

graycopy = gray.copy()
graycopy2 = gray.copy()

# REMOVE RET
ret, contours, heirarchy= cv2.findContours(thresh1,cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx =cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
    
    cv2.drawContours(graycopy, [approx], 0, (0,255,0), 0)
    
    if len(approx)==4 and 400.0>cv2.contourArea(approx)>100:
        
        M=cv2.moments(approx)
        cX=int(M["m10"]/M["m00"])
        cY=int(M["m01"]/M["m00"])
        
        cv2.circle(graycopy2, (cX, cY), 2, (0, 255, 0), -1)
    
        cv2.drawContours(graycopy2, [approx], 0, (0,255,0), 0)
        print(cv2.contourArea(approx))
        
        WPCONTOUR = approx
cv2.imshow("img with contours", graycopy)
cv2.imwrite("withcontours.jpg", graycopy)
cv2.imshow("Image with rectangles", graycopy2)
cv2.imwrite("waypoint.jpg", graycopy2)

try:

    # extract region of image with waypoint
    x, y, w, h = cv2.boundingRect(WPCONTOUR)
    minimg = thresh1[y:y+h, x:x+w]
    
    testmin = gray[y:y+h, x:x+w]
    
    cv2.imshow("small", testmin)
    
    # REMOVE RET
    ret, contours, heirarchy = cv2.findContours(minimg, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        approx =cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        cv2.drawContours(testmin, [approx], 0, (0,255,255), 0)
        AREA_ARRAY.append(cv2.contourArea(approx))
    
    cv2.imshow("sklcn", testmin)
    
    ind = AREA_ARRAY.index(min(AREA_ARRAY))
    
    LETTER_CNT=cv2.approxPolyDP(contours[ind], 0.05*cv2.arcLength(contours[ind], True), True)
    print(len(LETTER_CNT))
    
    if len(LETTER_CNT) == 5 or len(LETTER_CNT) == 6:
        LETTER = "L"
    else:
        LETTER = "X"
    
    print("LETTER: ", LETTER)
    
except:
    print("No waypoint")

# close windows
cv2.waitKey(0)
cv2.destroyAllWindows()
