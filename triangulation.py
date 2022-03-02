import numpy as np

def find_depth(shape_right, shape_left, frame_right, frame_left, baseline, f, alpha):

    # Converting FOCAL LENGTH (f) from [mm] to [pixel]
    height_left, width_left, depth_left = frame_left.shape
    height_right, width_right, depth_right = frame_right.shape

    # Standard formula for [mm] to [pixel] conversion
    if width_left == width_right:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
    else:
        print("Left and right camera frames do not have the same pixel width")

    # Getting x coordinate of left and right shape
    # xL and xR
    x_left = shape_left[0]
    x_right = shape_right[0]

    # Calculating the DISPARITY
    # d = xL - xR
    disparity = x_left - x_right


    # Calculating the DEPTH
    # Z = (b * f) / d
    zDepth = (baseline * f_pixel) / disparity

    return abs(zDepth)
