import pygame
import Camera
import cv2
import numpy as np

def is_overlapping(surface1, surface2):
    offset_x = surface1.get_rect[0] - surface2.get_rect[0]
    offset_y = surface1.get_rect[1] - surface2.get_rect[1]
    
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    return mask1.overlap(mask2, (offset_x,offset_y))

def find_midpoint(p1, p2):
    return [int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2)]

class Ball(pygame.sprite.Sprite):
    def __init__(self, r=10, w=20, h=20, color=(255,0,0)):
        super().__init__()

        self.image = pygame.Surface([w, h], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, find_midpoint([0,0],[w,h]), r)

        self.rect = self.image.get_rect()

class Hand(pygame.sprite.Sprite):
    def __init__(self, points, res=(640,480)):
        super().__init__()
        self.res = res

        self.image = pygame.Surface(self.res, pygame.SRCALPHA)

        self.update(points)
    
    def update(self, points):
        temp = pygame.Surface(self.res, pygame.SRCALPHA)
        pygame.draw.polygon(temp, (0, 128, 255), hand)
        self.image = temp

class Game(pygame.sprite.Sprite):
    def __init__(self, cam=0, res=(640,480)):
        if cam == 0:
            cam = Camera.Camera()
        self.cam = cam
        
        self.res = res

        self.ball = Ball()
        self.update_hands()
    
        pygame.init()
        self.screen = pygame.display.set_mode(res)
        self.clock = pygame.time.Clock()

    def clear_screen(self, color=(0,0,0)):
        """Clears screen by filling it with a color"""
        self.screen.fill(color)

    def update_hands(self):
        """Updates hand objects to reflect current frame"""
        self.cam.set_frame()
        points = self.cam.get_hands()

        self.hands = []
        for hand in points:
            temp = pygame.Surface(self.res, pygame.SRCALPHA)
            pygame.draw.polygon(temp, (0, 128, 255), hand)
            self.hands.append(temp)

    def update_screen(self):
        """Updates display to include all hands found in the image"""
        self.screen.blit(self.ball.image, [0,0])

        for hand in self.hands:
            self.screen.blit(hand, [0,0])

    def display_screen(self, rate=60, flip=0):
        """Displays screen surface and returns boolean value"""
        cont = False

        # tests to see if window was closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cont = True

        pygame.display.flip()
        self.clock.tick(rate)
        return cont
    
    def update(self):
        """Updates the screen and returns boolean value"""
        self.clear_screen()
        self.update_hands()
        self.update_screen()
        return self.display_screen()

def main():
    game = Game()

    done = False
    # main loop that updates the frame
    while not done:
        done = game.update()

        # loads opencv frame
        cv2.imshow("frame", game.cam.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__": 
    main()