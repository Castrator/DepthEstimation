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
    l_b_l = np.array([143, 110, 50])
    u_b_l = np.array([255, 255, 255])
    l_b_r = np.array([143, 110, 50])
    u_b_r = np.array([255, 255, 255])

    if (camera == 2):
        mask = cv2.inRange(hsv, l_b_l, u_b_l)
    else:
        mask = cv2.inRange(hsv, l_b_r, u_b_r)

    # Noise removal
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask