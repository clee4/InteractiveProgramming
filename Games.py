import pygame
import Camera
import cv2
import numpy as np
import random

def is_overlapping(surface1, surface2):
    """Returns point at which two surfaces first overlap"""
    return pygame.sprite.collide_mask(surface1, surface2)

def find_midpoint(p1, p2):
    """returns the midpoint of two points"""
    return [int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2)]

class Ball(pygame.sprite.Sprite):
    def __init__(self, r=25, w=50, h=50, color=(0,255,0)):
        super().__init__()

        self.r = 25
        self.w = w
        self.h = h

        self.color = color

        self.image = pygame.Surface([self.w, self.h], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, find_midpoint([0,0],[self.w,self.h]), self.r)

        self.rect = self.image.get_rect()

    def move(self, point):
        """Moves ball to different location"""
        point = [point[0]-(self.w/2), point[1]-(self.h/2)]
        self.rect.x = point[0]
        self.rect.y = point[1]
    
    def update_color(self, color):
        self.color = color
        self.image = pygame.Surface([self.w, self.h], pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, find_midpoint([0,0],[self.w,self.h]), self.r)

class Hand(pygame.sprite.Sprite):
    def __init__(self, points, res=(640,480)):
        super().__init__()
        self.res = res

        self.image = pygame.Surface(self.res, pygame.SRCALPHA)

        self.update(points)

        self.rect = self.image.get_rect()
    
    def update(self, points):
        """Redraws hand approximations"""
        temp = pygame.Surface(self.res, pygame.SRCALPHA)
        pygame.draw.polygon(temp, (0, 128, 255), points)
        self.image = temp

class Game(pygame.sprite.Sprite):
    def __init__(self, cam=0, res=(640,480)):
        if cam == 0:
            cam = Camera.Camera()
        self.cam = cam
        
        self.res = res

        self.ball = Ball()
        self.update_hands()
    
        self.time = pygame.time.get_ticks()
        self.curtime = 0
        self.score = 0
        self.highscore = 0

        self.playing = False

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        pygame.init()
        self.screen = pygame.display.set_mode(res)
        self.clock = pygame.time.Clock()

    def reset(self):
        """Resets game and waits to restart"""
        self.time = pygame.time.get_ticks()
        self.score = 0
        self.ball.move((0,0))
        self.playing = False
        self.ball.update_color((0,255,0))

    def clear_screen(self, color=(0,0,0)):
        """Clears screen by filling it with a color"""
        self.screen.fill(color)

    def update_hands(self):
        """Updates hand objects to reflect current frame"""
        self.cam.set_frame()
        points = self.cam.get_hands()

        self.hands = []
        for hand in points:
            self.hands.append(Hand(hand))

    def update_time(self):
        """Updates current time"""
        self.curtime = (pygame.time.get_ticks()-self.time)/1000

    def update_text(self):
        """Updates score ant time text"""
        textsurface = self.myfont.render('Score: '+str(self.score), False, (255, 255, 255))
        self.screen.blit(textsurface, [10,10])
        timesurface = self.myfont.render('Time: '+str(int(self.curtime))+"s", False, (255, 255, 255))
        self.screen.blit(timesurface, [250,10])

    def update_highscore(self):
        """Updates high score"""
        if self.score > self.highscore:
            self.highscore = self.score
        scoresurface = self.myfont.render('High Score: '+str(self.highscore), False, (255, 255, 255))
        self.screen.blit(scoresurface, [475,10])

    def update_screen(self):
        """Updates display to include all hands found in the image"""
        self.screen.blit(self.ball.image, [self.ball.rect.x,self.ball.rect.y])

        for hand in self.hands:
            self.screen.blit(hand.image, [0,0])

            count = 0
            while is_overlapping(hand, self.ball) != None:
                count+=1
                self.ball.move((random.randint(0,640),random.randint(0,480)))

            if count != 0 and self.playing:
                self.score+=1
            elif count!= 0 and not self.playing:
                self.playing = True
                self.time = pygame.time.get_ticks()
                self.ball.update_color((255,0,0))

        if self.playing:
            self.update_time()

        self.update_highscore()
        self.update_text()

        if self.curtime >= 10:
            self.reset()
        
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