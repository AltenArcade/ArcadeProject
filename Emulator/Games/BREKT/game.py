from platform import system
from os import path
import pygame
import Games.BREKT.classes as cl
import Games.BREKT.levels as lvl
import numpy as np
import random as rn
import time
from Games.BREKT.InputName import InputName
from InputReader import InputReader

class Game:
    def __init__(self, screen, width, height, y_offset, bg_screen, clock, high_score, hs_block_list):
        self.screen = screen
        self.bg_screen = bg_screen
        self.width = width
        self.height = height
        self.y_offset = y_offset
        self.clock = clock

        # NEW ----------------------------------------------------------------------------------------------------------
        if system() == "Windows":
            self.path = str(path.dirname(path.realpath(__file__))) + "\\"
        if system() == "Linux":
            self.path = str(path.dirname(path.realpath(__file__))) + "/"
        self.hs_block_list = hs_block_list
        self.input_reader = InputReader()
        self.prev_input = None
        # --------------------------------------------------------------------------------------------------------------

        # NEW ----------------------------------------------------------------------------------------------------------
        self.vel = 12  # 8 * width / 1600
        # --------------------------------------------------------------------------------------------------------------
        self.dv = 0
        self.v_tmp = 0

        self.score = 0

        # NEW ---------------------------------------------------------------------------------------------------------- 
        self.name = " "
        self.font = pygame.font.SysFont('Calibri', int(self.height / 15), True, False)
        self.font = pygame.font.Font(self.path + 'font.ttf', int(self.height / 22))
        self.drop_probability = 0.25
        # --------------------------------------------------------------------------------------------------------------

        self.level = 1
        self.lives = 4
        self.not_died_count = 1
        self.done = False
        self.next = False

        self.bp = self.construct_bp(self.level)

        self.ball = None
        self.ball_r = int(self.width / 160)
        self.pad = None
        self.reversed_keys = False

        self.obj_list = pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.all_list = pygame.sprite.Group()
        self.badge_list = pygame.sprite.GroupSingle()
        self.drop_list = pygame.sprite.Group()
        self.ball_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()

        self.badge = pygame.sprite.Sprite()
        self.badge.image = pygame.Surface([self.width, self.height / 4])
        self.badge.image.fill(cl.GREY)
        self.badge.rect = self.badge.image.get_rect()
        self.badge.rect.x = 0
        self.badge.rect.y = self.height / 2 - self.badge.rect.height / 2
        self.badge_list.add(self.badge)

        # SOUND

        # self.bullet_fired = pygame.mixer.Sound("bullet_fired.wav")

        # NEW ----------------------------------------------------------------------------------------------------------
        self.high_score = high_score
        # --------------------------------------------------------------------------------------------------------------

        # INITIATE LEVEL
        self.initiate_level()

    def initiate_level(self):
        self.done = False
        self.next = False

        self.bp = self.construct_bp(self.level)

        # INITIATE BLOCKS
        block_w = self.width / len(self.bp[0])
        block_h = self.height / (len(self.bp[0]) * 1.5)
        for i in range(len(self.bp)):
            for j in range(len(self.bp[i])):
                if self.bp[i][j] != 0:
                    pos_x = block_w / 2 + j * block_w
                    pos_y = self.y_offset + block_h / 2 + i * block_h
                    b = cl.Block(self.bp[i][j], block_w - self.width / 400, block_h - self.height / 250, pos_x, pos_y)
                    if self.bp[i][j] != 5:
                        self.block_list.add(b)
                    self.obj_list.add(b)
                    self.all_list.add(b)

        # INITIATE PAD
        self.pad = cl.Pad(self.width / 14, block_h, self.width / 2, self.height - self.height / 32, self.vel)
        self.obj_list.add(self.pad)
        self.all_list.add(self.pad)

        # INITIATE BALL
        self.ball = cl.Ball(self.pad, self.ball_r, self.pad.rect.center[0],
                            self.pad.rect.center[1] - (self.pad.rect.height / 2) * 1.1,
                            self.width, self.height, self.vel, False)
        self.ball_list.add(self.ball)
        self.all_list.add(self.ball)

        # INITIATE INFO
        self.info = cl.Info(self.y_offset, self.width, self.path)
        self.all_list.add(self.info)

        # DRAW FIRST TIME
        self.redraw()

        # LEVEL TEXT
        self.badge_list.draw(self.screen)
        #font = pygame.font.SysFont('Calibri', int(self.height / 5), True, False)
        font = pygame.font.Font(self.path + 'font.ttf', int(self.height / 7))
        text = font.render(str(self.level), True, cl.BLACK)
        self.screen.blit(text, [(self.width / 2) - text.get_rect().width / 2, (self.height / 2) -
                                  text.get_rect().height / 2])
        pygame.display.flip()
        time.sleep(2)
        pygame.event.clear()

        # INITIATE MAIN LOOP
        self.update()

    def update(self):
        self.pad.dx = self.v_tmp
        while not self.done:
            # Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                action = self.input_reader.readInput(event)
                if action is not None and action[0] == 0:
                    action = action[1]
                    if action == "left":
                        self.dv = (1 - 2 * self.reversed_keys) * self.vel
                        self.pad.dx -= self.dv
                        self.prev_input = "left"
                    elif action == "right":
                        self.dv = (1 - 2 * self.reversed_keys) * self.vel
                        self.pad.dx += self.dv
                        self.prev_input = "right"
                    elif action == "execute":
                        if self.pad.has_canon and len(self.bullet_list) == 0:
                            for i in range(0, 2):
                                bullet = cl.Bullet(self.pad, i)
                                self.bullet_list.add(bullet)
                        if not self.ball.started:
                            self.ball.started = True
                            tmp_dx = -1 + rn.random() * 2
                            tmp_dy = -1
                            self.ball.dx = int((tmp_dx / np.sqrt(tmp_dx ** 2 + tmp_dy ** 2)) * self.vel)
                            self.ball.dy = int((tmp_dy / np.sqrt(tmp_dx ** 2 + tmp_dy ** 2)) * self.vel)
                            #self.ball.dx = 0
                            #self.ball.dy = -self.vel
                    elif action == "back":
                        self.done = True
                    elif action == "center":
                        if self.prev_input == "left":
                            #self.pad.dx += (1 - 2 * self.reversed_keys) * self.vel
                            self.pad.dx += self.dv
                        elif self.prev_input == "right":
                            #self.pad.dx -= (1 - 2 * self.reversed_keys) * self.vel
                            self.pad.dx -= self.dv
                        self.prev_input = None

            # Game logic
            self.pad.move()
            self.check_pad_wall_collision()
            for ball in self.ball_list:
                self.check_ball_obj_collision(ball)
                self.check_ball_wall_collision(ball)
                ball.move()

            for bullet in self.bullet_list:
                self.check_bullet_obj_collision(bullet)
                self.check_bullet_wall_collision(bullet)
                bullet.move()

            self.check_drop_collision()
            for drop in self.drop_list:
                drop.move()

            # Check if level is completed
            if len(self.block_list) == 0:
                self.done = True
                self.next = True

            # Redraw
            self.redraw()

            self.clock.tick(60)

        if self.next:
            self.score += self.not_died_count * self.level * 100
            self.not_died_count += 1

            self.reset()
            self.clean_up()

            # NEW ------------------------------------------------------------------------------------------------------
            if self.level > 4:
                self.game_completed()
                if self.check_if_high_score():
                    self.get_player_name()
                    self.insert_score()
                    self.save_score()
                    self.high_score = self.get_high_score()
                    self.show_high_score()
                self.clean_up()
                #self.game_completed()
            else:
                self.level += 1
                self.initiate_level()
            #-----------------------------------------------------------------------------------------------------------

            #self.level += 1
            #self.initiate_level()
        else:
            self.game_over()
            if self.check_if_high_score():
                self.get_player_name()
                self.insert_score()
                self.save_score()
                self.high_score = self.get_high_score()
                self.show_high_score()
            self.clean_up()

    def redraw(self):
        self.screen.blit(self.bg_screen, (0, 0))
        self.info.update(self.level, self.score, self.lives)
        self.bullet_list.draw(self.screen)
        self.all_list.draw(self.screen)
        pygame.display.flip()

    def draw_pad(self):
        self.pad.draw()

    def construct_bp(self, level):
        if level <= len(lvl.bp):
            str = lvl.bp[level-1]
        else:
            str = lvl.bp[0]
        bp = []
        tmp = []
        for chr in str:
            if chr == ' ':
                tmp.append(0)
            elif chr != '-':
                tmp.append(int(chr))
            else:
                bp.append(tmp)
                tmp = []
        return bp

    def check_ball_obj_collision(self, ball):
        collided = False
        collide_list = pygame.sprite.spritecollide(ball, self.obj_list, False)
        for obj in collide_list:
            if not collided:
                obj_x = obj.rect.center[0]
                obj_y = obj.rect.center[1]
                ball_x = ball.rect.center[0]
                ball_y = ball.rect.center[1]
                if abs(ball_y - obj_y) < obj.rect.height / 2:
                    ball.dx = int(-ball.dx)
                if abs(ball_x - obj_x) < obj.rect.width / 2:
                    if isinstance(obj, cl.Pad):
                        #self.ball.dy = int(-self.ball.dy)
                        f = 0.38 * (self.pad.dx != 0)
                        tmp_dx = int((1-f) * ball.dx - f * self.pad.dx)
                        tmp_dy = int(-ball.dy)
                        ball.dx = int((tmp_dx / np.sqrt(tmp_dx ** 2 + tmp_dy ** 2)) * self.vel)
                        ball.dy = int((tmp_dy / np.sqrt(tmp_dx ** 2 + tmp_dy ** 2)) * self.vel)
                    else:
                        ball.dy = int(-ball.dy)
                else:
                    ball.dx = int(-ball.dx)  # Must be fixed
                    ball.dy = int(-ball.dy)
                collided = True

            if isinstance(obj, cl.Block):
                self.score += obj.give_points()
                if obj.hp > 1:
                    obj.hit()
                else:
                    if rn.random() <= obj.type * self.drop_probability:
                        drop = cl.Drop(obj.width, obj.height, rn.randrange(0, 7), obj.rect.center, self.vel, self.path)
                        self.drop_list.add(drop)
                        self.all_list.add(drop)
                    self.block_list.remove(obj)
                    self.obj_list.remove(obj)
                    self.all_list.remove(obj)

    def check_ball_wall_collision(self, ball):
        if ball.rect.y < self.y_offset:
            ball.dy = int(-ball.dy)
        elif ball.rect.y + ball.radius > self.pad.rect.y: #ball.rect.y + 2 * ball.radius > self.height:
            if self.lives > 1:
                self.not_died_count = 0
                self.lives -= 1
                self.redraw()
                time.sleep(2)
                self.reset()
                pygame.event.clear()
            else:
                self.done = True
        elif ball.rect.x < 0 or ball.rect.x + 2 * ball.radius > self.width:
            ball.dx = int(-ball.dx)

    def check_pad_wall_collision(self):
        if self.pad.rect.x < 0:
            self.pad.rect.x = 0
        elif self.pad.rect.x > self.width - self.pad.rect.width:
            self.pad.rect.x = self.width - self.pad.rect.width

    def check_drop_collision(self):
        for drop in self.drop_list:
            if drop.rect.y == self.height:
                self.drop_list.remove(drop)
                self.all_list.remove(drop)

        collide_list = pygame.sprite.spritecollide(self.pad, self.drop_list, False)
        for drop in collide_list:
            self.drop_list.remove(drop)
            self.all_list.remove(drop)
            if drop.type == 0:
                self.lives += 1
            elif drop.type == 1:
                ball = cl.Ball(self, self.ball_r, self.width / 2, self.y_offset + 2 * self.ball_r, self.width, self.height, self.vel, True)
                self.ball_list.add(ball)
                self.all_list.add(ball)
            elif drop.type == 2:
                self.pad.extend_width()
            elif drop.type == 3:
                self.pad.reduce_width()
            elif drop.type == 4:
                if self.lives > 1:
                    self.not_died_count = 0
                    self.lives -= 1
                    self.redraw()
                    time.sleep(2)
                    self.reset()
                    pygame.event.clear()
                else:
                    self.done = True
            elif drop.type == 5:
                self.reversed_keys = not self.reversed_keys
                self.pad.dx = -self.pad.dx
                self.dv = -self.dv
            elif drop.type == 6:
                self.pad.has_canon = True
                self.pad.draw()

    def check_bullet_wall_collision(self, bullet):
        if bullet.rect.y < 0:
            self.bullet_list.remove(bullet)
            self.all_list.remove(bullet)

    def check_bullet_obj_collision(self, bullet):
        collide_list = pygame.sprite.spritecollide(bullet, self.obj_list, False)
        for obj in collide_list:
            if isinstance(obj, cl.Block):
                self.score += obj.give_points()
                if obj.hp > 1:
                    obj.hit()
                else:
                    if rn.random() <= obj.type * self.drop_probability:
                        drop = cl.Drop(obj.width, obj.height, rn.randrange(0, 7), obj.rect.center, self.vel, self.path)
                        self.drop_list.add(drop)
                        self.all_list.add(drop)
                    self.block_list.remove(obj)
                    self.obj_list.remove(obj)
                    self.all_list.remove(obj)
                self.bullet_list.remove(bullet)  # Change here if you want the bullets to not collide with type 5 blocks

    def game_over(self):
        # self.screen.blit(self.bg_screen, (0, 0))
        self.redraw()

        self.badge_list.draw(self.screen)
        #font = pygame.font.SysFont('Calibri', int(self.height / 5), True, False)
        font = pygame.font.Font(self.path + 'font.ttf', int(self.height / 7))
        text = font.render("GAME OVER", True, cl.BLACK)
        self.screen.blit(text, [(self.width / 2) - text.get_rect().width / 2, (self.height / 2) -
                                  text.get_rect().height / 2])
        pygame.display.flip()
        #time.sleep(3)
        while True:
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    return

    def clean_up(self):
        self.drop_list.empty()
        self.block_list.empty()
        self.obj_list.empty()
        self.ball_list.empty()
        self.bullet_list.empty()
        self.all_list.empty()

    def reset(self):
        if self.reversed_keys:
            self.pad.dx = -self.pad.dx
            self.dv = -self.dv
            self.reversed_keys = False

        self.v_tmp = self.pad.dx

        self.pad.dx = 0
        self.v_tmp = 0
        self.prev_input = None

        self.ball.reset()
        self.all_list.remove(self.ball_list)
        self.ball_list.empty()
        self.all_list.add(self.ball)
        self.ball_list.add(self.ball)

        self.all_list.remove(self.drop_list)
        self.drop_list.empty()

        self.all_list.remove(self.bullet_list)
        self.bullet_list.empty()

        self.pad.reset()
        self.redraw()


    # NEW --------------------------------------------------------------------------------------------------------------
    def game_completed(self):
        self.screen.blit(self.bg_screen, (0, 0))
        self.redraw()

        self.badge_list.draw(self.screen)
        #font = pygame.font.SysFont('Calibri', int(self.height / 10), True, False)
        font = pygame.font.Font(self.path + 'font.ttf', int(self.height / 20))
        text = font.render("WINNER WINNER CHICKEN DINNER!", True, cl.BLACK)
        self.screen.blit(text, [(self.width / 2) - text.get_rect().width / 2, (self.height / 2) -
                                  text.get_rect().height / 2])
        pygame.display.flip()
        time.sleep(2)
        
    def get_high_score(self):
        file = open(self.path + "high_score.txt", "r")
        lst = [l.split(":") for l in file.readlines()]
        for t in lst:
            try:
                t[1] = int(t[1])
            except ValueError:
                print("Error can not be integer")
        s = sorted(lst, key=lambda score: score[1])[::-1]
        file.close()
        return s

    def show_high_score(self):
        self.screen.blit(self.bg_screen, (0, 0))
        self.hs_block_list.draw(self.screen)
        pixel_offset = int(self.height / 12)
        i = 0

        for score in self.high_score:
            string = score[0] + "  " + str(score[1])
            txt = self.font.render(string, 1, cl.WHITE)
            self.screen.blit(txt, ((self.width - self.font.size(string)[0]) / 2,
                                   2 * self.y_offset + (i * pixel_offset)))
            i += 1
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    return
        
    def check_if_high_score(self):
        for score in self.high_score:
            if self.score > score[1] or len(self.high_score) < 10:
                return True
        return False
        
    def get_player_name(self):
        name_module = InputName(self.screen, self.bg_screen, self.score, self.font, self.input_reader)
        self.name = name_module.GetPlayerName()
        
    def insert_score(self):
        for i in range(len(self.high_score)):
            if self.high_score[i][1] < self.score:
                self.high_score.insert(i, [self.name, self.score])
                break
        self.high_score = sorted(self.high_score, key=lambda score: score[1])[::-1]
        while len(self.high_score) > 10:
            self.high_score.remove(self.high_score[len(self.high_score) - 1])

    def set_high_score(self):
        self.insert_score()
        return self.high_score

    def save_score(self):
        file = open(self.path + "high_score.txt", "w")
        for item in self.high_score:
            file.write(item[0] + ":" + str(item[1]) + "\n")
        file.close()
    #---------------------------------------------------------------------------------------------------------------
