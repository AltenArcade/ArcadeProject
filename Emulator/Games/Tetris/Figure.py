import pygame
from Games.Tetris.Block import Block
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)

class Figure(pygame.sprite.Sprite):
    def __init__(self, struct,width,height,block,prediction):
        super().__init__()
        self.board_width = width
        self.board_height = height
        self.block_size = block
        self.color_list = [GREEN,RED,PURPLE,YELLOW,PINK]
        self.matrix = struct
        self.block_list = pygame.sprite.Group()
        self.is_moving = True
        if prediction:
            fig_w = len(self.matrix[0]) * self.block_size
            fig_h = len(self.matrix) * self.block_size
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if (self.matrix[i][j] != 0):
                        block = Block(self.block_size, color = self.color_list[randint(0,len(self.color_list)-1)])
                        block.rect.x = j * self.block_size + (self.board_width - fig_w) / 2
                        block.rect.y = i * self.block_size + (self.board_height - fig_h) / 2
                        self.block_list.add(block)
        else:
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if (self.matrix[i][j] != 0):
                        block = Block(self.block_size, color = self.color_list[randint(0,len(self.color_list)-1)])
                        block.rect.x = j * self.block_size + self.board_width / 2
                        block.rect.y = i * self.block_size
                        self.block_list.add(block)

    def GetShape(self):
        return self.matrix

    def CorrectSide(self):
        for block in self.block_list.sprites():
            if block.rect.x + self.block_size > self.board_width:
                self.block_list.update("left")
            if block.rect.x < 0:
                self.block_list.update("right")

    def IsMoving(self):
        return self.is_moving

    def CheckCollision(self, collision_list, case):

        self.block_list.update(case)
        if (len(pygame.sprite.groupcollide(self.block_list, collision_list, False, False)) > 0):
            self.block_list.update("reset " + case)
            if case == "down":
                self.is_moving = False
            return False
        else:
            self.block_list.update("reset " + case)
            return True

    def CheckBottom(self):
        for block in self.block_list.sprites():
            if block.rect.y + self.block_size >= self.board_height:
                self.is_moving = False
                return False
        return True

    def flip(self):
        old_y = self.block_list.sprites()[0].rect.y
        old_x = self.block_list.sprites()[0].rect.x
        self.block_list = pygame.sprite.Group()
        self.matrix = [list(a) for a in zip(*self.matrix[::-1])]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if (self.matrix[i][j] != 0):
                    block = Block(self.block_size, color = self.color_list[randint(0,len(self.color_list)-1)])
                    block.rect.x = j * self.block_size + old_x
                    block.rect.y = i * self.block_size + old_y
                    self.block_list.add(block)

    def move_down(self):
        self.block_list.update("down")

    def move_left(self):
        move = True
        for block in self.block_list.sprites():
            if block.rect.x <= 0:
                move = False
                break
        if move:
            self.block_list.update("left")

    def move_right(self):
        move = True
        for block in self.block_list.sprites():
            if block.rect.x + self.block_size >= self.board_width:
                move = False
                break
        if move:
            self.block_list.update("right")
