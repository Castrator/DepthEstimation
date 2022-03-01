import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt

# Functions
import HSV_filter as hsv
import shape_recognition as shape
import triangulation as tri

# Opening of cameras - (Comment out to use SAMPLE IMAGES)
cap_left = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap_right = cv2.VideoCapture(4, cv2.CAP_DSHOW)

# Uncomment to use SAMPLE IMAGES
# cap_left = cv2.imread('DepthEstimation/images/im1.png')
# cap_right = cv2.imread('DepthEstimation/images/im2.png')

frame_rate = 120

B = 9                   # Distance between the cameras [cm]
f = 6                   # Camera Lense's focal length [mm]
alpha = 56.6            # Camera field of view in the horizontal plane [degrees]

count = -1

while(True):
    count += 1

    # Reading camera data (Comment out to use SAMPLE IMAGES)
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    # Uncomment to use SAMPLE IMAGES
    # ret_left = True
    # frame_left = cv2.imread('DepthEstimation/images/im1.png')
    # ret_right = True
    # frame_right = cv2.imread('DepthEstimation/images/im2.png')

    if ret_right == False or ret_left == False:
        break
    else:
        # Applying HSV FILTER
        mask_left = hsv.add_HSV_filter(frame_left, 2)
        mask_right = hsv.add_HSV_filter(frame_right, 4)

        # RESULT FRAMES after applying HSV-filter mask
        res_left = cv2.bitwise_and(frame_left, frame_left, mask=mask_left)
        res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
        
        # Applying SHAPE RECOGNITION
        circles_left = shape.find_circles(frame_left, mask_left)
        circles_right = shape.find_circles(frame_right, mask_right)

        # CALCULATING DEPTH
        if np.all(circles_right) == None or np.all(circles_left) == None:
            cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        else:
            
            depth = tri.find_depth(circles_right, circles_left, frame_right, frame_left, B, f, alpha)

            cv2.putText(frame_left, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,255), 2)
            cv2.putText(frame_right, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,255), 2)
            cv2.putText(frame_left, "Distance: " +  str(round(depth,3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.putText(frame_right, "Distance: " + str(round(depth,3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            print("Depth: ", depth)
    
    cv2.imshow("Frame Left", frame_left)
    cv2.imshow("Frame Right", frame_right)
    cv2.imshow("Mask Left", mask_left)
    cv2.imshow("Mask Right", mask_right)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# DESTROY all windows
cap_left.release()
cap_right.release()

cv2.destroyAllWindows()

