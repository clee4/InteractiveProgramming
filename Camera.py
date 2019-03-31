import cv2
import numpy as np 

class Camera:
    def __init__(self, cam_num = 0):
        # creates camera
        self.cap = cv2.VideoCapture(cam_num)

        # saves first frame as background
        _, self.background = self.cap.read()
        _, self.frame = self.cap.read()

        # 
        self.fgbg = cv2.createBackgroundSubtractorKNN()

        # upper and lower skin threshold values
        self.lower_skin = np.array([54, 131, 110])
        self.upper_skin = np.array([163, 157, 135])

        # haar cascade to be used for detecting faces
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

        # 5x5 kernel to used for morphologies
        self.kernel = np.ones((5,5), np.uint8)
    
    def get_frame(self):
        _, frame = self.cap.read()
        return frame

    def to_gray(self, img):
        """returns grayscale version of img"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def to_HSV(self, img):
        """returns hsv version of i    def to_HSVmg"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def to_YCrCb(self, img):
        """returns ycrcb version of img"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    def blur(self, img, k_size=(5,5)):
        # img = cv2.medianBlur(img, 5)
        return cv2.GaussianBlur(img, k_size, 0)

    def remove_background(self, img, back=0):
        """
        Takes image in RGB then converts to YCrCb and removes background from img.

        returns frame without a background in YCrCb
        """
        # if back == 0:
        #     back = self.background
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY) 
        # fore = cv2.absdiff(img, back)
        # _, mask = cv2.threshold(fore, 45, 255, cv2.THRESH_BINARY)
        # return mask
        fgmask = self.fgbg.apply(img)
        return cv2.bitwise_and(img, img, mask=fgmask)

    def remove_face(self, img, cascade=0):
        """
        Finds face using haar cascade then fills it with a color
        """
        if cascade == 0:
            cascade = self.face_cascade

        faces = cascade.detectMultiScale(img, scaleFactor=1.2, minSize=(20, 20))
        
        mask = np.ones(img.shape[0:2], dtype="uint8")*255
        for x, y, w, h in faces:
            mask = cv2.rectangle(mask, (x,y), (x+w,y+h), (0,0,0), -1)
        
        return cv2.bitwise_and(img, img, mask= mask)

    def detect_edge(self, img, sigma=.33):
        # compute the median of the single channel pixel intensities
        v = np.median(img)
    
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
    
        # return the edged image
        edges = cv2.Canny(img, lower, upper)
        return edges

    def find_contours(self, img):
        img = self.to_gray(img)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        hull = []
 
        # calculate points for each contour
        for i in range(len(contours)):
            # creating convex hull object for each contour
            hull.append(cv2.convexHull(contours[i], False))

        # create an empty black image
        drawing = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        
        # draw contours and hull points
        for i in range(len(contours)):
            color_contours = (0, 255, 0) # green - color for contours
            color = (255, 0, 0) # blue - color for convex hull
            # draw ith contour
            cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)
            # draw ith convex hull object
            cv2.drawContours(drawing, hull, i, color, 1, 8)
        return hull


    def close(self, img):
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, self.kernel)

    def open(self, img):
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, self.kernel)

    def remove_noise(self, img, i=2):
        """cv2.addWeighted(img, .5, edges, .5, 0)
        Remcv2.addWeighted(img, .5, edges, .5, 0) to make it more useable

        imgcv2.addWeighted(img, .5, edges, .5, 0) to remove noise from
        i: cv2.addWeighted(img, .5, edges, .5, 0)s to erode and dilate

        returns less noisy frame
        """
        return self.close(self.open(self.close(img)))

    def in_range(self, img):
        temp = self.to_YCrCb(img)
        mask = cv2.inRange(temp, self.lower_skin, self.upper_skin)
        return cv2.bitwise_and(img, img, mask=mask)

    def get_hands(self, img):
        """returns finds masks out hands"""
        frame = img
        frame = self.blur(frame)
        frame = self.remove_face(frame)
        frame = self.remove_background(frame)
        frame = self.in_range(frame)
        frame =self.remove_noise(frame)
        frame =self.close(frame)
        # frame = self.detect_edge(frame,.7)
        print(self.find_contours(frame))
        
        
        return frame

if __name__ == "__main__":
    cam = Camera()
    while 1:
        frame = cam.get_frame()
        frame = cam.get_hands(frame)

        cv2.imshow("frame", cv2.flip(frame,1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



