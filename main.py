import cv2
import numpy as np

# Functions
import HSV_filter as hsv
import shape_recognition as shape
import triangulation as tri

# Opening of cameras - (Comment out to use SAMPLE IMAGES)
# Replace parameter in VideoCapture() with your camera indices
cap_left = cv2.VideoCapture(2)
cap_right = cv2.VideoCapture(4)

# Uncomment to use SAMPLE IMAGES
# cap_left = cv2.imread('DepthEstimation/images/im1.png')
# cap_right = cv2.imread('DepthEstimation/images/im2.png')

frame_rate = 120

# Replace values accordingly for best results
B = 9                  # Distance between the cameras [cm]
f = 6                   # Camera Lense's focal length [mm]
alpha = 56.6            # Camera field of view in the horizontal plane [degrees]

while(True):
    # Reading camera data (Comment out to use SAMPLE IMAGES)
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    # Uncomment to use SAMPLE IMAGES
    # ret_left = True
    # frame_left = cv2.imread('DepthEstimation/images/im1.png')
    # ret_right = True
    # frame_right = cv2.imread('DepthEstimation/images/im2.png')
    
    # Applying HSV FILTER
    mask_left = hsv.add_HSV_filter(frame_left, 2)
    mask_right = hsv.add_HSV_filter(frame_right, 4)

    # RESULT FRAMES after applying HSV-filter mask
    res_left = cv2.bitwise_and(frame_left, frame_left, mask=mask_left)
    res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
    
    # Applying SHAPE RECOGNITION
    shape_left = shape.find_shape(frame_left, mask_left, 'rectangle')
    shape_right = shape.find_shape(frame_right, mask_right, 'rectangle')

    # Calculating DEPTH
    if np.all(shape_right) == None or np.all(shape_left) == None:
        cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    else:
        depth = tri.find_depth(shape_right, shape_left, frame_right, frame_left, B, f, alpha)
        # print("Depth: ", depth)
        
        cv2.putText(frame_left, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50,230,0), 2)
        cv2.putText(frame_right, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50,230,0), 2)
        cv2.putText(frame_left, "Distance: " +  str(round(depth,3)) + " cm", (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50,230,0), 2)
        cv2.putText(frame_right, "Distance: " + str(round(depth,3)) + " cm", (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50,230,0), 2)
        
    # HSV to BGR
    mask_left = cv2.cvtColor(mask_left, cv2.COLOR_GRAY2BGR)
    mask_right = cv2.cvtColor(mask_right, cv2.COLOR_GRAY2BGR)
    
    # Stacking the frames
    left = np.hstack([frame_left, frame_right])
    right = np.hstack([mask_left, mask_right])

    stacked = np.vstack([left, right])

    # Displaying stacked frames
    cv2.imshow("Depth Estimation", stacked)
    
    k = cv2.waitKey(1)
    if  k == ord('q'):
        break

# DESTROY all windows
cap_left.release()
cap_right.release()

cv2.destroyAllWindows()

