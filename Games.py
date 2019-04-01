import pygame
import Camera
import cv2
import numpy as np

class Hands:
    def __init__(self, cam=0, res=(640,480)):
        # inits camera for hand detection
        if cam == 0:
            cam = Camera.Camera()
        
        self.cam = cam
        
        pygame.init()
        self.screen = pygame.display.set_mode(res)
        self.clock = pygame.time.Clock()
    
    def clear_screen(self, color=(0,0,0)):
        self.screen.fill(color)
    
    def draw_hands(self):
        # updates camera frame and gets hands coordinates
        self.cam.set_frame()
        hands = self.cam.get_hands()
        if len(hands) != 0 and  len(hands[0]) > 2:
            for hand in hands:
                pygame.draw.polygon(self.screen, (0, 128, 255), hand)
    
    def display_screen(self, rate=60, flip=0):
        cont = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cont = True

        pygame.display.flip()
        self.clock.tick(rate)
        return cont
    
    def update(self):
        self.clear_screen()
        self.draw_hands()
        return self.display_screen()

def main():
    hand = Hands()

    done = False
    # main loop that updates the frame
    while not done:
        done = hand.update()

        # loads opencv frame
        cv2.imshow("frame", hand.cam.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__": 
    main()