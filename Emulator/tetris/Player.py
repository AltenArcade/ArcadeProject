import pygame
from os import path
from random import randint
from tetris.Figure import Figure

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)

FPS = 60

class Player:

    def __init__(self, clk, nr, logo, screen, blocks):
        self.name = ""
        self.screen = screen
        self.board_width = screen.get_size()[0]
        self.board_height = screen.get_size()[1]
        self.full_row = blocks
        self.block_size = (self.board_width / blocks)
        self.logo = logo
        self.score = 0
        self.font = pygame.font.Font(path.abspath("font.ttf"), 20)
        self.clock = clk
        self.player_number = nr

        self.collision_list = pygame.sprite.Group()
        self.game_over = False
        self.run_game = True
        self.restart = False
        self.frame_ctr = 0
        self.speed_control = 1
        self.empty_row_effect = pygame.mixer.Sound(path.abspath("tetris\\Sweep5.wav"))
        self.current_figure = Figure(self.GetFigureShape(),self.board_width,self.board_height,self.block_size)


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
            if y_coords.count(element) > self.full_row:
                print("FAIL")
            if y_coords.count(element) == self.full_row:
                self.speed_control += 1
                delete_rows.append(element)
        self.score += len(delete_rows)
        for row in delete_rows:
            for block in blocklist:
                if block.rect.y == row:
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

    def GetPlayerName(self):
        pixel_offset = 70
        text = ["New High Score of " + str(self.score), "Type your name: "]
        for i in range(len(text)):
            rect = (((self.board_width - self.font.size(text[i])[0]) / 2), (
                (self.board_height - self.font.size(text[i])[1] - pixel_offset) / 2) + i * pixel_offset)
            txt = self.font.render(text[i], 1, WHITE)
            self.screen.blit(txt, rect)

        rect = list(rect)
        rect[1] += pixel_offset
        self.EnterName(rect[1])

    def EnterName(self, y_pos):

        box_x = 160
        box_y = 20
        enter_box = pygame.Surface((box_x,box_y))
        text_position = ((self.board_width - box_x) / 2, y_pos)
        enter_box.fill(BLACK)
        pygame.draw.rect(enter_box,BLACK,(0,0,box_x,box_y),1)
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:len(self.name)-1]
                    else:
                        if len(self.name) < 8:
                            self.name += str(event.unicode)
            text = self.font.render(self.name, 1, WHITE)
            r = text.get_rect()
            enter_box.blit(text, r)
            self.screen.blit(enter_box, text_position)
            enter_box.fill(BLACK)
            pygame.display.flip()

    def move(self):

        if not self.current_figure.IsMoving():
            self.collision_list.add(self.current_figure.block_list)
            self.collision_list = self.CheckFullRow(self.collision_list,self.empty_row_effect)
            self.game_over = self.CheckIfGameOver(self.current_figure)
            self.current_figure = Figure(self.GetFigureShape(),self.board_width,self.board_height,self.block_size)

        if (self.frame_ctr >= (int(FPS / self.speed_control)) - 1 and self.current_figure.CheckCollision(self.collision_list, "down")):
            self.frame_ctr = 0
            self.current_figure.move_down()

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
        if self.current_figure.CheckCollision(self.collision_list, "down"):
            self.current_figure.move_down()

    def CheckGameOver(self):
        return self.game_over

    def CheckIfHighScore(self,high_score):
        for score in high_score:
            if self.score > score[1]:
                return True
        return False