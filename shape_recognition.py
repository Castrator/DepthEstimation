import cv2
import imutils

def find_shape(frame, mask, shape):

    # Finding the contours
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sorting the contours
    contours = imutils.grab_contours(contours)
    
    # Inital value is none
    center = None

    if len(contours) > 0:
        # Taking the largest contour in the mask (biggest area)
        max_contour = max(contours, key=cv2.contourArea)

        # Finding the centroid
        M = cv2.moments(max_contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        center = (cX, cY)
        print(center)

        match shape:
            case 'rectangle':
                draw_rectangle(frame, max_contour)
            case 'circle':
                draw_circle(frame, max_contour)

    print(len(contours))
    print(center)
    return center

def draw_rectangle(frame, contour):
    # Retrieving details on the bounding rectangle
    (x,y,w,h) = cv2.boundingRect(contour)

    # Drawing the rectangle
    cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,255,255), 2)

def draw_circle(frame, contour):
    # Finding the minimum enclosing circle
    ((x,y), radius) = cv2.minEnclosingCircle(contour)

    # Only proceed if the radius is > than a minimum value
    if radius > 10:
        # Drawing the circle in the centroid on the frame
        cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
