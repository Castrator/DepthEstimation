# Depth Estimation with OpenCV <br/>
Code Reference:
https://www.youtube.com/watch?v=t3LOey68Xpg

![image](https://user-images.githubusercontent.com/72141153/156124728-ad30f63a-c35b-42ee-a6f9-4b3af498d67a.png)

## Algorithm Flow

The `main.py` will handle the process flow. 
We start off by initiating the video capture of our two cameras. 
### _HSV Conversion:_<br/>
From the video capture, in `HSV_filter.py`, the frame goes through:<br/>
* blurring
* BGR to HSV 
* masking with HSV with desired color (blue is default)
* noise removal

https://youtu.be/fHmkWt7SWSs?t=31

### _Shape Recognition:_<br/>
After masking, we proceed to detecting the shapes in the frame in `shape_recognition.py` via:
* finding the contours
* sorting the contours
* finding the centroid
* drawing a shape around the contour

https://pyimagesearch.com/2016/02/01/opencv-center-of-contour/
https://stackoverflow.com/questions/40203932/drawing-a-rectangle-around-all-contours-in-opencv-python

### _Triangulation:_<br/>
Once the shape is recognized, we begin triangulation in `triangulation.py` by:<br/>
* converting **focal point (f)** from _mm_ to _pixel_
* retrieving **xL** and **xR**
* calculating the **disparity** where _d = xL - xR_
* calculating the **depth** where _Z = (b * f) / d_

After undergoing these 3 processes, the masked frames are then converted back to BGR so that it can be stacked with the other frames and shown in 1 window. To end the program, simply press _q_.

![image](https://user-images.githubusercontent.com/72141153/156321423-fd31c495-9466-4c54-a890-8d349a1900f0.png)

