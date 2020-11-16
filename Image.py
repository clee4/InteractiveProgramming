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
    """
    lower: lower YCrCb bound for color
    upper: upper YCrCb bound for color

    returns everythings in frame between lower and upper
    """
    temp = to_YCrCb(img)
    mask = cv2.inRange(temp, lower, upper)
    img = cv2.bitwise_and(img, img, mask=mask)
    return img, mask

#######################
# Cleans up the image #
#######################
def blur_img(img, k_size=(5,5)):
    """returns a gaussian blur of the image"""
    return cv2.GaussianBlur(img, k_size, 0)

def close_img(img, kernel=kernel):
    """returns image with closed shapes"""
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def open_img(img, kernel=kernel):
    """returns image with removed outer nosie"""
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def remove_noise(img, i=2):
    """returns less noisy frame"""
    return close_img(open_img(close_img(img)))

#######################################################
# Finds polygons of where hands are using convex hull #
#######################################################
def simplify_points(points):
    """
    Converts nested points found using convex hull to more usable organization
    
    returns reorganized points
    """
    new = []
    for shape in points:
        temp = []
        for i in range(len(shape)):
            temp.append((shape[i][0][0],shape[i][0][1]))
        new.append(temp)
    
    return new

def get_contours(img, thresh = 1750):
    """returns points of polygon approximation of contours"""
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    # create hull array for convex hull points
    hull = []
    points = []
    
    # calculate points for each contour
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull.append(cv2.convexHull(contours[i], False))

    color_contours = (0, 255, 0) # green - color for contours
    color = (255, 0, 0) # blue - color for convex hull
    # draw contours and hull points
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > thresh:
            # draw ith contour
            cv2.drawContours(img, contours, i, color_contours, 1, 8, hierarchy)
            # draw ith convex hull object
            cv2.drawContours(img, hull, i, color, 1, 8)

            points.append(hull[i].tolist())

    return img, simplify_points(points)