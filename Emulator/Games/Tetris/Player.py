import pygame
from os import path
from platform import system
from random import randint
from Option import Option
from InputReader import InputReader
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

    def __init__(self, clk, nr, logo, screen, pred, block_count):
        if system() == "Windows":
            self.path = str(path.dirname(path.realpath(__file__))) + "\\"
        if system() == "Linux":
            self.path = str(path.dirname(path.realpath(__file__))) + "/"
        self.clock = clk
        self.player_number = nr
        self.figure_prediction = pred
        self.screen = screen
        self.logo = logo
        self.name = ""
        self.score = 0
        self.board_width = screen.get_size()[0]
        self.board_height = screen.get_size()[1]
        self.full_row_def = block_count
        self.block_size = (self.board_width / block_count)
        self.font = pygame.font.Font(self.path + "/font.ttf", 17)
        self.collision_list = pygame.sprite.Group()
        self.game_over = False
        self.frame_ctr = 0
        self.speed_control = 1
        self.empty_row_effect = pygame.mixer.Sound(self.path + "Sweep5.wav")
        self.current_figure = Figure(self.GetFigureShape(), self.board_width, self.board_height, self.block_size, False)
        self.next_figure = Figure(self.GetFigureShape(), self.figure_prediction.get_size()[0],
                                  self.figure_prediction.get_size()[1], self.block_size / 2, True)
        self.options = []
        # Variables for redirecting the speed control in multiplayer mode
        self.redir_speed = False
        self.old_score = 0

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
        for block in blocklist:
            y_coords.append(block.rect.y)
        y_coords.sort()
        y_coords_unique = list(set(y_coords))
        for element in y_coords_unique:
            if y_coords.count(element) == self.full_row_def:
                delete_rows.append(element)
        self.score += len(delete_rows)

        for row in delete_rows:
            for block in blocklist:
                if block.rect.y == row:
                    block.Draw(WHITE)
                    blocklist.remove(block)

        delete_rows.sort()
        while len(delete_rows) is not 0:
            sound.play()
            for block in blocklist:
                if block.rect.y < delete_rows[0]:
                    block.rect.y += self.block_size

            delete_rows = delete_rows[1:len(delete_rows)]

        return blocklist

    def CheckIfGameOver(self, figure):
        for block in figure.block_list:
            if block.rect.y == 0:
                return True
        return False

    def DrawScore(self):
        message = "Score: " + str(self.score)
        text = self.font.render(message, 1, WHITE)
        rec = text.get_rect(center=(self.board_width / 2, 50))
        self.screen.blit(text, rec)

    def GameOver(self):
        pixel_offset = 70
        self.screen.fill(BLACK)
        text = ["GAME OVER", "Press ESC to cancel..."]
        for i in range(len(text)):
            txt = self.font.render(text[i], 1, WHITE)
            pos_x = ((self.board_width - self.font.size(text[i])[0]) / 2)
            pos_y = ((self.board_height - self.font.size(text[i])[1] - pixel_offset) / 2) + i * pixel_offset
            self.screen.blit(txt, (pos_x, pos_y))

    def GetPlayerName(self, reader):
        name_module = InputName(self.screen, self.score, self.font)
        self.name = name_module.GetPlayerName(reader)

    # Called when both players are alive. The speed is proportional to the opponents score
    def SetOpponentSpeedControl(self, score):
        self.speed_control = 1 + score * 0.5

    # If one player is dead, the speed will be proportional to the players own score
    def SetOwnSpeedControl(self, opponent_score):
        if not self.redir_speed:  # This should happen only once to save the current score of the player.
            self.old_score = self.score
            self.speed_control = 1 + (opponent_score + (self.score - self.old_score)) * 0.5
            self.redir_speed = True
        # Increment the speed control with the difference between the current score and the score when the opponent died
        else:
            self.speed_control = 1 + (opponent_score + (self.score - self.old_score)) * 0.5

    def move(self):

        if not self.current_figure.IsMoving():
            self.collision_list.add(self.current_figure.block_list)
            self.collision_list = self.CheckFullRow(self.collision_list, self.empty_row_effect)
            self.game_over = self.CheckIfGameOver(self.current_figure)
            self.current_figure = Figure(self.next_figure.GetShape(), self.board_width,
                                         self.board_height, self.block_size, False)
            self.next_figure = Figure(self.GetFigureShape(), self.figure_prediction.get_size()[0],
                                      self.figure_prediction.get_size()[1], self.block_size / 2, True)

        if self.frame_ctr >= (int(FPS / self.speed_control)) - 1 \
                and self.current_figure.CheckCollision(self.collision_list, "down") \
                and self.current_figure.CheckBottom():

            self.frame_ctr = 0
            self.current_figure.move_down()

        self.next_figure.block_list.draw(self.figure_prediction)
        self.current_figure.block_list.draw(self.screen)
        self.collision_list.draw(self.screen)
        #self.DrawEndPosition()

        self.DrawScore()
        self.frame_ctr += 1

    '''def DrawEndPosition(self):
        pos = []
        figure = Figure(self.current_figure.GetShape(),self.board_width,self.board_height, self.block_size, False)
        figure.AddPos(self.current_figure)
        while figure.CheckCollision(self.collision_list, "down") and figure.CheckBottom():
            figure.move_down()
        for block in figure.block_list:
            pos.append((block.rect.x, block.rect.y))
        i = 0
        for block in figure.block_list:
            pygame.draw.rect(self.screen, WHITE, [pos[i][0], pos[i][1], figure.block_size, figure.block_size])
            i += 1
        for block in figure.block_list:
            print(block.rect.x)
            pygame.draw.rect(self.screen,WHITE,[block.rect.x,block.rect.y,figure.block_size,figure.block_size],1)'''

    def CheckIfExit(self):
        idx = 0
        x_offset = 30
        y_offset = 50
        text = self.font.render("Quit Game?", 1, WHITE)
        pos = ((self.board_width - self.font.size("Yes")[0]) / 2) - x_offset, (self.board_height / 2) + y_offset
        opt1 = Option("Yes", pos, self.screen, self.font, RED, WHITE)

        pos = ((self.board_width - self.font.size("No")[0]) / 2) + x_offset, (self.board_height / 2) + y_offset
        opt2 = Option("No", pos, self.screen, self.font, RED, WHITE)

        self.options = [opt1, opt2]
        self.options[0].hovered = True
        input_reader = InputReader()
        while True:
            for event in pygame.event.get():
                action = input_reader.readInput(event)
                if action is not None:
                    if action[1] == 'left':
                        idx = self.ChangeOption(action[1], idx)
                    elif action[1] == 'right':
                        idx = self.ChangeOption(action[1], idx)
                    elif action[1] == 'execute':
                        if self.options[idx].text == 'Yes':
                            return False
                        else:
                            return True
            self.next_figure.block_list.draw(self.figure_prediction)
            self.current_figure.block_list.draw(self.screen)
            self.collision_list.draw(self.screen)
            self.screen.blit(text, ((self.board_width - text.get_size()[0]) / 2, self.board_height / 2))
            self.DrawScore()
            for option in self.options:
                option.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def ChangeOption(self, case, idx):
        if case == 'left':
            self.options[idx].hovered = False
            idx -= 1
            if idx < 0:
                idx = len(self.options) - 1
            self.options[idx].hovered = True
        elif case == 'right':
            self.options[idx].hovered = False
            idx += 1
            if idx > len(self.options) - 1:
                idx = 0
            self.options[idx].hovered = True
        return idx

    def flip(self):
        if self.current_figure.CheckCollision(self.collision_list, "left") \
                and self.current_figure.CheckCollision(self.collision_list, "right") \
                and self.current_figure.CheckCollision(self.collision_list, "down"):

            self.current_figure.flip()
            self.current_figure.CorrectSide()

    def left(self):
        if self.current_figure.CheckCollision(self.collision_list, "left"):
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

    def CheckIfHighScore(self, high_score):
        if len(high_score) == 0:
            return True
        for score in high_score:
            if self.score > score[1] or len(high_score) < 5:
                return True
        return False