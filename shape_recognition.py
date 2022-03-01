import sys
import cv2
import numpy as np
import time
import imutils

def find_circles(frame, mask):

    # Finding the contours
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sorting the contours
    contours = imutils.grab_contours(contours)
    
    # Inital value is none
    center = None

    # if no object is found return None
    if len(contours) > 0:
        # Taking the largest contour in the mask (biggest area)
        c = max(contours, key=cv2.contourArea)

        # Finding the minimum enclosing circle
        ((x,y), radius) = cv2.minEnclosingCircle(c)

        # Finding the centroid
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius is > than a minimum value
        # to disable tracking on unwanted objects
        if radius > 10:
            # Drawing the circle in the centroid on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            
            # Updating the list of tracked points
            cv2.circle(frame, center, 5, (0,0,0), -1)

    return center
