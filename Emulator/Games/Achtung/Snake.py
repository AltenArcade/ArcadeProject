import os, sys
import pygame
from pygame.locals import *


class Snake(pygame.sprite.Sprite):
    """ The snake that moves around the screen """

    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = 16
        self.height = 16
        self.color = color#(255, 51, 51)
        self.pellet_width = 8
        self.pellet_height = 8

        """ Head """
        self.image = pygame.Surface((self.width, self.height))#pygame.image.load('snake.png')
        self.rect = self.image.get_rect()
        #self.rect.x = 10 * self.width
        self.rect.x = x
        #self.rect.y = 10 * self.height
        self.rect.y = y
        self.image.fill(self.color)

        """ Tail """
        self.tailImage = []
        self.tailRect = []

        self.length = 3
        self.pellets = 0
        self.score = 0
        self.score_tick = 0
        self.x_dist = self.width
        self.y_dist = self.height
        self.current_dir = 'right'
        self.speed = 1
        self.next_move = pygame.Rect(self.rect.x + self.width, self.rect.y, self.width, self.height)
        self.banned_move = None
        self.stunned = 0
        self.stun_time = 10
        self.key_registered = False

        for i in range(self.length):
            self.tailImage.append(pygame.Surface((self.width, self.height)))
            self.tailRect.append(self.tailImage[-1].get_rect())


    def move(self):
        xMove = 0
        yMove = 0

        if(self.stunned == 0):
            """ Update movement of tail """
            for i in range(len(self.tailRect)-1, -1, -1):
                if(i == 0):
                    self.tailRect[i].x = self.rect.x
                    self.tailRect[i].y = self.rect.y
                else:
                    self.tailRect[i].x = self.tailRect[i-1].x
                    self.tailRect[i].y = self.tailRect[i-1].y

            """ Update movement of head """
            if(self.current_dir == 'right' and self.banned_move != 'right'):
                xMove = self.x_dist
            elif(self.current_dir == 'left' and self.banned_move != 'left'):
                xMove = -self.x_dist
            elif(self.current_dir == 'up' and self.banned_move != 'up'):
                yMove = -self.y_dist
            elif(self.current_dir == 'down' and self.banned_move != 'down'):
                yMove = self.y_dist

            self.rect.move_ip(xMove, yMove)
        else:
            self.stunned -= 1


    def setDirection(self, key):

        if (key != None):
            if ((key == K_RIGHT or key == K_d) and self.banned_move != 'right' and self.current_dir != 'left'):
                self.current_dir = 'right'
                self.next_move.x = self.rect.x + self.width
                self.next_move.y = self.rect.y
            elif ((key == K_LEFT or key == K_a) and self.banned_move != 'left' and self.current_dir != 'right'):
                self.current_dir = 'left'
                self.next_move.x = self.rect.x - self.width
                self.next_move.y = self.rect.y
            elif ((key == K_UP or key == K_w) and self.banned_move != 'up' and self.current_dir != 'down'):
                self.current_dir = 'up'
                self.next_move.x = self.rect.x
                self.next_move.y = self.rect.y - self.height
            elif ((key == K_DOWN or key == K_s) and self.banned_move != 'down' and self.current_dir != 'up'):
                self.current_dir = 'down'
                self.next_move.x = self.rect.x
                self.next_move.y = self.rect.y + self.height

    def checkTailCollision(self):
        return self.rect.collidelist(self.tailRect) != -1

    def checkSnakeCollision(self, snake):
        return self.rect.collidelist(snake.tailRect) != -1


class Pellet(pygame.sprite.Sprite):
    """ Pellet that the snake picks up """

    def __init__(self, rect = None):
        pygame.sprite.Sprite.__init__(self)
        self.width = 8
        self.height = 8
        self.color = (51, 51, 255)
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image.fill(self.color)
        if rect != None:
            self.rect = rect


class Wall(pygame.sprite.Sprite):
    """ Wall at the sides of the screen """

    def __init__(self, image = None, rect = None, loc = None):
        pygame.sprite.Sprite.__init__(self)
        self.thickness = 20
        self.color = (255, 51, 51)
        #self.image = pygame.Surface((self.width, self.height))
        #self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect
        if loc != None:
            self.loc = loc
        if image != None:
            self.image = image
            self.image.fill(self.color)
