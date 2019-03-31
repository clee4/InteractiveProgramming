import cv2
import numpy as np

kernel = np.ones((5,5), np.uint8)

##########################
# Changes color of image #
##########################
def to_gray(img):
    """returns grayscale version of img"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def to_HSV(img):
    """returns hsv version of i    def to_HSVmg"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def to_YCrCb(img):
    """returns ycrcb version of img"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

def in_range(img, lower, upper):
        mask = cv2.inRange(img, lower, upper)
        return cv2.bitwise_and(img, img, mask=mask), mask

#######################
# Cleans up the image #
#######################
def blur_img(img, k_size=(5,5)):
    # img = cv2.medianBlur(img, 5)
    return cv2.GaussianBlur(img, k_size, 0)

def close_img(img, kernel=kernel):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def open_img(img, kernel=kernel):
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def remove_noise(img, i=2):
    """cv2.addWeighted(img, .5, edges, .5, 0)
    Remcv2.addWeighted(img, .5, edges, .5, 0) to make it more useable

    imgcv2.addWeighted(img, .5, edges, .5, 0) to remove noise from
    i: cv2.addWeighted(img, .5, edges, .5, 0)s to erode and dilate

    returns less noisy frame
    """
    return close_img(open_img(close_img(img)))

#######################################################
# Finds polygons of where hands are using convex hull #
#######################################################
def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # create hull array for convex hull points
    hull = []
    
    # calculate points for each contour
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull.append(cv2.convexHull(contours[i], False))

    # create an empty black image
    drawing = img.copy()
    
    # draw contours and hull points
    for i in range(len(contours)):
        color_contours = (0, 255, 0) # green - color for contours
        color = (255, 0, 0) # blue - color for convex hull
        # draw ith contour
        cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)
        # draw ith convex hull object
        cv2.drawContours(drawing, hull, i, color, 1, 8)

    return img, hull