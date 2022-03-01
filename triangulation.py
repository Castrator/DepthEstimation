import sys
import cv2
from cv2 import circle
import numpy as np
import time

def find_depth(circles_right, circles_left, frame_right, frame_left, baseline, f, alpha):

    # Converting focal length (f) from [mm] to [pixel]
    height_left, width_left, depth_left = frame_left.shape
    height_right, width_right, depth_right = frame_right.shape

    if width_left == width_right:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
    else:
        print("Left and right camera frames do not have the same pixel width")

    x_left = circles_left[0]
    x_right = circles_right[0]

    # Calculating the DISPARITY
    disparity = x_left - x_right

    # Calculating the DEPTH
    zDepth = (baseline * f_pixel) / disparity

    return abs(zDepth)
