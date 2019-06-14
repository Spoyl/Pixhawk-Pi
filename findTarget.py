# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 19:26:10 2019

@author: Oliver
"""

import cv2
import numpy as np

IMAGE_DIR = "C:\\Users\\Oliver\\Desktop\\DroneVisionSystem\\Drone Gopro Pictures\\"
IMAGE_NAME = "G0058905.JPG"     #3648x2736
SCALE_PERCENT = 20

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

# Show resized image
#cv2.imshow("original image (20% downsized)",resized)

# Show green channel
#g = resized.copy()
#g[:, :, 0] = 0
#g[:, :, 1] = 0
#cv2.imshow("image",g)

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)    #convert to grayscale
#cv2.imshow("grayscale image", gray)

ret, thresh1 = cv2.threshold(gray,210,255,cv2.THRESH_BINARY)    #threshold
cv2.imshow("thresholded image", thresh1)

#edges = cv2.Canny(thresh1,0, 255)   # find edges
#cv2.imshow("edges", edges)

graycopy = gray.copy()
graycopy2 = gray.copy()

img_cont, contours, heirarchy= cv2.findContours(thresh1,cv2.RETR_TREE,
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

cv2.imshow("Image with contours", graycopy)
cv2.imshow("Image with rectangles", graycopy2)


cv2.waitKey(0)
cv2.destroyAllWindows() 