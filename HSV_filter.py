import sys
import cv2
import numpy as np
import time

def add_HSV_filter(frame, camera):
    # Blurring the frame
    blur = cv2.GaussianBlur(frame, (5,5), 0)

    # BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Assigning LOWERBOUND and UPPERBOUND for left and right cameras
    
    # BLUE
    lower_bound = np.array([100,100,80])
    upper_bound = np.array([140,250,250])

    # RED
    # lower_bound = np.array([160,100,100])
    # upper_bound = np.array([180,250,250])

    # GREEN
    # lower_bound = np.array([40,80,100])
    # upper_bound = np.array([80,250,250])

    if (camera == 2):
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
    else:
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Noise removal
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask