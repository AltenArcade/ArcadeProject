import pygame
import numpy as np
import random as rn

# Properties
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
YELLOW_DARK = (124, 124, 0)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)
block_colors = [GREEN, YELLOW, ORANGE, RED, GREY]


class Block(pygame.sprite.Sprite):
    def __init__(self, i, w, h, pos_x, pos_y): # Block typ can be 1,2,3,4
        super().__init__()

        self.width = w
        self.height = h
        self.hp = i
        self.type = i
        self.color = block_colors[self.hp-1]

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

        self.draw()

    def hit(self):
        if self.hp != 5:
            self.hp -= 1
            self.color = block_colors[self.hp-1]
            self.draw()

    def draw(self):
        pygame.draw.rect(self.image, self.color,
                         [0, 0, self.width, self.height], 0)

    def give_points(self):
        p = 0
        for i in range(self.hp, self.type+1):
            p += i
        return p * (self.type != 5)


class Pad(pygame.sprite.Sprite):
    def __init__(self, w, h, pos_x, pos_y, vel):  # Block typ can be 1,2,3
        super().__init__()
        self.w = w
        self.h = h
        self.res_x = pos_x
        self.res_y = pos_y
        self.color = WHITE
        self.dx = 0
        self.vel = vel
        self.has_canon = False

        self.image = pygame.Surface([w, h])

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

        self.draw()

    def draw(self):
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        self.image.fill(WHITE)
        if self.has_canon:
            a=1
            pygame.draw.polygon(self.image, GREY, [[self.w / 8, 0], [0, 0], [0, self.h]])
            pygame.draw.polygon(self.image, GREY, [[self.rect.width - self.w / 8, 0],
                                                   [self.rect.width, 0], [self.rect.width, self.h]])

    def move(self):
        self.rect.x += self.dx

    def extend_width(self):
        center = self.rect.center
        self.rect.width *= 2
        self.rect.center = center
        self.draw()

    def reduce_width(self):
        center = self.rect.center
        self.rect.width /= 2
        self.rect.center = center
        self.draw()

    def reset(self):
        self.has_canon = False
        center = self.rect.center
        self.rect.width = self.w
        self.rect.center = center
        self.draw()


class Ball(pygame.sprite.Sprite):
    def __init__(self, pad, r, pos_x, pos_y, width, height, vel, is_extra_ball):  # Block typ can be 1,2,3
        super().__init__()

        self.pad = pad

        self.started = is_extra_ball
        self.radius = r
        self.vel = vel
        self.res_x = pos_x
        self.res_y = pos_y
        self.color = WHITE
        self.scr_width = width
        self.scr_height = height
        self.dx = 0
        self.dy = 0

        dx = -1 + rn.random()*2
        dy = -1

        self.dx = is_extra_ball * int((dx / np.sqrt(dx ** 2 + dy ** 2)) * self.vel)
        self.dy = is_extra_ball * int((dy / np.sqrt(dx ** 2 + dy ** 2)) * self.vel)

        self.image = pygame.Surface([2 * self.radius, 2 * self.radius])
        self.image.fill(GREY)
        self.image.set_colorkey(GREY)

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y - self.radius)  # +220 , +40 only for test

        self.draw()

    def draw(self):
        pygame.draw.ellipse(self.image, self.color, [0, 0, 2 * self.radius, 2 * self.radius])

    def move(self):
        if not self.started:
            self.rect.x = self.pad.rect.center[0] - self.radius
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy

    def reset(self):
        self.rect.center = (self.pad.rect.center[0], self.res_y - self.radius)
        self.dx = 0
        self.dy = 0
        self.started = False


class Info(pygame.sprite.Sprite):
    def __init__(self, y_offset, width, path):
        super().__init__()
        self.size = y_offset
        self.font_size = int(self.size * 0.8 * 0.8)
        self.width = width
        self.path = path

        self.image = pygame.Surface([self.width, self.size])
        self.image.fill(GREY)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        #self.font = pygame.font.SysFont('Calibri', self.font_size, True, False)
        self.font = pygame.font.Font(self.path + 'font.ttf', self.font_size)
        self.score_text = self.font.render("SCORE:", True, BLACK)
        self.level_text = self.font.render("LEVEL:", True, BLACK)

    def update(self, lv, sc, liv):
        score = self.font.render(str(sc), True, BLACK)
        level = self.font.render(str(lv), True, BLACK)
        lives = self.font.render(str((liv-1)*'O'), True, BLACK)

        self.image.fill(GREY)

        self.image.blit(self.score_text, [(self.size - self.font_size) / 2 + self.size * 0.6, (self.size - self.font_size) / 2])
        self.image.blit(score, [(self.size - self.font_size) + self.size * 0.6 +
                                     self.score_text.get_rect().width, (self.size - self.font_size) / 2])

        self.image.blit(level, [self.image.get_rect().center[0] - level.get_rect().width / 2,
                                self.image.get_rect().center[1] - level.get_rect().height / 2])

        self.image.blit(lives, [self.width - lives.get_rect().width - + self.size * 0.6, (self.size - self.font_size) / 2])

class Drop(pygame.sprite.Sprite):
    def __init__(self, w, h, type, block_center, vel, path):
        super().__init__()

        self.width = 0.8 * w
        self.height = 0.8 * h
        self.path = path

        #
        self.type = type
        self.texts = [chr(9675), str(chr(9675)+chr(9675)), str(chr(8592) + chr(8594)),
                      str(chr(8594) + chr(8592)), "X", "?", "--¤"]
        self.texts = ["O", "OO", str(chr(8592) + chr(8594)),
                      str(chr(8594) + chr(8592)), "X", "?", "++"]
        self.font = pygame.font.SysFont('Calibri', int(self.height * 1.2), True, False)
        self.font = pygame.font.Font(self.path + 'font.ttf', int(self.height*0.9))
        self.font.set_bold(True)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.center = block_center
        self.dy = vel * 0.5

        self.draw()

    def draw(self):
        self.image.fill(WHITE)
        text = self.font.render(self.texts[self.type], True, BLACK)
        self.image.blit(text, [(self.width - text.get_rect().width) / 2, (self.height - text.get_rect().height*0.8) / 2])

    def move(self):
        self.rect.y += self.dy


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pad, pos):
        super().__init__()
        self.w = pad.w / 40
        self.h = pad.h
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = (pad.rect.center[0] - (1 - pos * 2)*(pad.rect.width / 2 - pad.w / 16), pad.rect.center[1])
        self.dy = -pad.vel*2

    def move(self):
        self.rect.y += self.dy
