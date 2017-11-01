from os import path
from platform import system
from random import randint

import pygame

from Games.Tetris.Figure import Figure
from Games.Tetris.InputName import InputName

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)

FPS = 60

class Player:

    def __init__(self, clk, nr, logo, screen, pred, blocks):
        if system() == "Windows":
            self.path = str(path.dirname(path.realpath(__file__))) + "\\"
        if system() == "Linux":
            self.path = str(path.dirname(path.realpath(__file__))) + "/"
        self.name = ""
        self.figure_prediction = pred
        self.screen = screen
        self.board_width = screen.get_size()[0]
        self.board_height = screen.get_size()[1]
        self.full_row = blocks
        self.block_size = (self.board_width / blocks)
        self.logo = logo
        self.score = 0
        self.font = pygame.font.Font(self.path + "/font.ttf", 17)
        self.clock = clk
        self.player_number = nr

        self.collision_list = pygame.sprite.Group()
        self.game_over = False
        self.run_game = True
        self.restart = False
        self.frame_ctr = 0
        self.speed_control = 1
        self.empty_row_effect = pygame.mixer.Sound(self.path + "Sweep5.wav")
        self.current_figure = Figure(self.GetFigureShape(),self.board_width,self.board_height,self.block_size, False)
        self.next_figure = Figure(self.GetFigureShape(),self.figure_prediction.get_size()[0],self.figure_prediction.get_size()[1],self.block_size / 2, True)

    def GetFigureShape(self):
        shapes = [
            [[0, 0, 1], [1, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 1, 0], [1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 1, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]]
        ]
        return shapes[randint(0, len(shapes) - 1)]

    def CheckFullRow(self, blocklist, sound):
        y_coords = []
        delete_rows = []
        self.empty_row = 0
        for block in blocklist:
            y_coords.append(block.rect.y)
        y_coords.sort()
        y_coords_unique = list(set(y_coords))
        for element in y_coords_unique:
            if y_coords.count(element) == self.full_row:
                #self.speed_control += 0.6
                delete_rows.append(element)
        self.score += len(delete_rows)

        for row in delete_rows:
            for block in blocklist:
                if block.rect.y == row:
                    block.Draw(WHITE)
                    blocklist.remove(block)

        delete_rows.sort()
        while(len(delete_rows) != 0):
            sound.play()
            for block in blocklist:
                if block.rect.y < delete_rows[0]:
                    block.rect.y += self.block_size

            delete_rows = delete_rows[1:len(delete_rows)]

        return blocklist

    def CheckIfGameOver(self,figure):
        for block in figure.block_list:
            if(block.rect.y == 0):
                return True
        return False

    def UpdateScore(self):
        message = "Score: " + str(self.score)
        text = self.font.render(message, 1, WHITE)
        rec = text.get_rect(center = (self.board_width / 2, 50))
        self.screen.blit(text, rec)

    def GameOver(self):
        pixel_offset = 70
        self.screen.fill(BLACK)
        text = ["GAME OVER","Press ESC to cancel..."]
        for i in range(len(text)):
            txt = self.font.render(text[i], 1, WHITE)
            self.screen.blit(txt, (((self.board_width - self.font.size(text[i])[0]) / 2), (
            (self.board_height - self.font.size(text[i])[1] - pixel_offset) / 2) + i * pixel_offset))

    def GetPlayerName(self,reader):
        name_module = InputName(self.screen,self.score,self.font)
        self.name = name_module.GetPlayerName(reader)

    def SetSpeedControl(self, score):
        self.speed_control = 1 + score * 0.5

    def move(self):

        if not self.current_figure.IsMoving():
            self.collision_list.add(self.current_figure.block_list)
            self.collision_list = self.CheckFullRow(self.collision_list,self.empty_row_effect)
            self.game_over = self.CheckIfGameOver(self.current_figure)
            self.current_figure = Figure(self.next_figure.GetShape(),self.board_width,self.board_height,self.block_size, False)
            self.next_figure = Figure(self.GetFigureShape(),self.figure_prediction.get_size()[0],self.figure_prediction.get_size()[1],self.block_size / 2, True)

        if (self.frame_ctr >= (int(FPS / self.speed_control)) - 1 and self.current_figure.CheckCollision(self.collision_list, "down") and self.current_figure.CheckBottom()):
            self.frame_ctr = 0
            self.current_figure.move_down()

        self.next_figure.block_list.draw(self.figure_prediction)
        self.current_figure.block_list.draw(self.screen)
        self.collision_list.draw(self.screen)

        self.UpdateScore()
        self.frame_ctr += 1

    def flip(self):
        self.current_figure.flip()
        self.current_figure.CorrectSide()

    def left(self):
        if self.current_figure.CheckCollision(self.collision_list,"left"):
            self.current_figure.move_left()

    def right(self):
        if self.current_figure.CheckCollision(self.collision_list, "right"):
            self.current_figure.move_right()

    def down(self):
        if self.current_figure.CheckCollision(self.collision_list, "down") and self.current_figure.CheckBottom():
            self.current_figure.move_down()

    def down_fast(self):
        while self.current_figure.CheckCollision(self.collision_list, "down") and self.current_figure.CheckBottom():
            self.current_figure.move_down()
            self.current_figure.block_list.draw(self.screen)

    def CheckGameOver(self):
        return self.game_over

    def CheckIfHighScore(self,high_score):
        for score in high_score:
            if self.score > score[1] or len(high_score) < 5:
                return True
        return False