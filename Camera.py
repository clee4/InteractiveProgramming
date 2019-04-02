import cv2
import numpy as np 
import Image as img

class Camera:
    def __init__(self, cam_num = 0):
        # creates camera
        self.cap = cv2.VideoCapture(cam_num)

        # sets initial frame
        _, self.frame = self.cap.read()

        # creates object for background subtraction
        self.fgbg = cv2.createBackgroundSubtractorKNN()

        # upper and lower skin threshold values
        self.lower_skin = np.array([54, 131, 110])
        self.upper_skin = np.array([163, 157, 135])

        # haar cascade to be used for detecting faces
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    
    def set_frame(self, flip=1):
        "Gets current frame"
        _, temp = self.cap.read()
        self.frame = cv2.flip(temp, flip)

    def remove_background(self, back=0):
        """
        Removes background of frame through OpenCV Background Subtraction
        """
        fgmask = self.fgbg.apply(self.frame)
        self.frame = cv2.bitwise_and(self.frame, self.frame, mask=fgmask)

    def find_face(self, cascade = 0):
        """
        Uses haar cascade to detect any faces in frame

        returns rectangles that bound the face
        """
        if cascade == 0:
            cascade = self.face_cascade

        return cascade.detectMultiScale(self.frame, scaleFactor=1.2, minSize=(20, 20))

    def remove_face(self):
        """
        Replaces each face with a black rectangle/square
        """
        faces = self.find_face()
        mask = np.ones(self.frame.shape[0:2], dtype="uint8")*255
        for x, y, w, h in faces:
            mask = cv2.rectangle(mask, (x,y), (x+w,y+h), (0,0,0), -1)
        
        self.frame = cv2.bitwise_and(self.frame, self.frame, mask= mask)

    def get_hands(self):
        """
        Masks out hands then finds convex hulls to approximate hands

        returns sets of points that approximates the hand
        """
        self.frame = img.blur_img(self.frame)
        self.remove_face()
        self.remove_background()
        self.frame = img.remove_noise(self.frame)
        self.frame = img.close_img(self.frame)
        self.frame, mask = img.in_range(self.frame, 
                                        self.lower_skin, 
                                        self.upper_skin)
        self.frame, points = img.get_contours(mask)
        
        return points

if __name__ == "__main__":
    cam = Camera()
    while 1:
        cam.set_frame()
        cam.get_hands()

        cv2.imshow("frame", cam.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



