import pygame
from platform import system
from os import path
from Games.Tetris.Player import Player
from Option import Option
from InputReader import InputReader

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)
GREY = (160, 160, 160)
WALL_SIZE = 20
FPS = 60


class Main:

    def __init__(self, screen):
        if system() == "Windows":
            self.path = str(path.dirname(path.realpath(__file__))) + "\\"
        if system() == "Linux":
            self.path = str(path.dirname(path.realpath(__file__))) + "/"
        self.run_game = False
        self.screen = screen
        self.board_width = self.screen.get_size()[0]
        self.board_height = self.screen.get_size()[1]
        self.logo = pygame.image.load(self.path + "Estetris_logo.png").convert_alpha()
        self.logo = self.ScaleImage(self.logo, self.board_width)
        self.screen_center = (self.board_width - self.logo.get_size()[0]) / 2
        self.exit_game = False
        self.restart = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(self.path + "font.ttf", 30)
        self.high_score = []
        self.options = []
        pygame.mixer.music.load(self.path + "tetris-sound.mp3")
        self.input_reader = InputReader()

    def start(self):
        self.high_score = self.GetHighScore()
        self.exit_game = False
        players = 0
        idx = 0
        self.DisplayOptions("Start", self.screen)
        pygame.mixer.music.play(-1)

        while not self.exit_game:
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    if action[1] == 'back':
                        self.exit_game = True
                    elif action[1] == 'up':
                        idx = self.ChangeOption(action[1], idx)
                    elif action[1] == 'down':
                        idx = self.ChangeOption(action[1], idx)
                    elif action[1] == 'execute':
                        if self.options[idx].text == "High Score":
                            self.ShowHighScore()
                        elif self.options[idx].text == "Exit":
                            self.exit_game = True
                        elif self.options[idx].text == "New Game":
                            players = self.GetPlayers(self.logo, self.screen_center)
                            self.run_game = True
            if self.run_game and players > 0:
                if players == 2:
                    self.TwoPlayer()
                else:
                    self.OnePlayer()
                    self.DisplayOptions("Start", self.screen)
                self.SaveScore()
            self.screen.blit(self.logo, (self.screen_center, self.board_height * 0.15))
            for option in self.options:
                option.draw()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
        pygame.mixer.music.stop()
        return

    def ScaleImage(self, img, width):

        img_ratio = img.get_rect().size[1] / img.get_rect().size[0]
        return pygame.transform.scale(img, (width, int(width * img_ratio)))

    def ChangeOption(self, case, idx):
        if case == 'up':
            self.options[idx].hovered = False
            idx -= 1
            if idx < 0:
                idx = len(self.options) - 1
            self.options[idx].hovered = True
        elif case == 'down':
            self.options[idx].hovered = False
            idx += 1
            if idx > len(self.options) - 1:
                idx = 0
            self.options[idx].hovered = True
        return idx

    def DisplayOptions(self, case, screen):
        self.options.clear()
        if case == "Start":
            text = ["New Game", "High Score", "Exit"]
            self.AddOptions(text, screen)
        elif case == "Exit":
            text = ["Yes", "No"]
            self.AddOptions(text, screen)
        self.options[0].hovered = True

    def GetHighScore(self):
        if path.isfile(self.path + "high_score.txt"):
            file = open(self.path + "high_score.txt", "r")
        else:
            file = open(self.path + "high_score.txt", "w+")
        lst = [l.split(":") for l in file.readlines()]
        for t in lst:
            try:
                t[1] = int(t[1])
            except ValueError:
                print("Error can not be integer")
        s = sorted(lst, key=lambda score: score[1])[::-1]
        file.close()
        return s

    def GetPlayers(self, logo, screen_center):
        done = False
        selection_font = pygame.font.Font(self.path + "font.ttf", 32)
        selection_font.set_underline(True)

        one_player = True
        start_string = "Players"
        text = self.font.render(start_string, 1, WHITE)
        y_offset = 50
        x_offset = 25
        while not done:
            self.screen.blit(logo, (screen_center, self.board_height * 0.15))
            self.screen.blit(text, ((self.board_width - self.font.size(start_string)[0]) / 2, self.board_height * 0.5))
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    action = action[1]
                    if action == 'back':
                        return 0
                    elif action == 'execute':
                        done = True
                    elif action == 'right':
                        one_player = False
                    elif action == 'left':
                        one_player = True
            txt_x = (self.board_width - self.font.size("1")[0]) / 2
            if one_player:
                self.screen.blit(selection_font.render("1", 1, WHITE),
                                 (txt_x - x_offset, self.board_height * 0.5 + y_offset))
                self.screen.blit(self.font.render("2", 1, WHITE),
                                 (txt_x + x_offset, self.board_height * 0.5 + y_offset))
            else:
                self.screen.blit(self.font.render("1", 1, WHITE),
                                 (txt_x - x_offset, self.board_height * 0.5 + y_offset))
                self.screen.blit(selection_font.render("2", 1, WHITE),
                                 (txt_x + x_offset, self.board_height * 0.5 + y_offset))

            pygame.display.flip()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

        if one_player:
            return 1
        else:
            return 2

    def KeyDown(self, action, player):
        if action == 'back':
            self.run_game = player.CheckIfExit()
        elif action == 'undo':
            player.flip()
        elif action == 'left':
            player.left()
        elif action == 'right':
            player.right()
        elif action == 'down':
            player.down()
        elif action == 'execute':
            player.down_fast()

    def InsertScore(self, high_score, player):
        if len(high_score) == 0:
            high_score.insert(0, [player.name, player.score])
        for i in range(len(high_score)):
            if high_score[i][1] < player.score or len(high_score) < 5:
                high_score.insert(i, [player.name, player.score])
                break
        high_score = sorted(high_score, key=lambda score: score[1])[::-1]
        while len(high_score) > 5:
            high_score.remove(high_score[len(high_score) - 1])
        return high_score

    def SetHighScore(self, player1, player2=None):
        if player2 is None:
            self.high_score = self.InsertScore(self.high_score, player1)
        else:
            if player1.score < player2.score:
                self.high_score = self.InsertScore(self.high_score, player1)
                self.high_score = self.InsertScore(self.high_score, player2)
            elif player1.score >= player2.score:
                self.high_score = self.InsertScore(self.high_score, player2)
                self.high_score = self.InsertScore(self.high_score, player1)
        return self.high_score

    def ShowHighScore(self):
        pixel_offset = 40
        i = 0
        self.screen.blit(self.logo, (self.screen_center, self.board_height * 0.15))
        for score in self.high_score:
            string = score[0] + " " + str(score[1])
            txt = self.font.render(string, 1, WHITE)
            pos_x = (self.board_width - self.font.size(string)[0]) / 2
            pos_y = self.board_height * 0.5 + (i * pixel_offset)
            self.screen.blit(txt, (pos_x, pos_y))
            i += 1
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    return

    def SaveScore(self):
        file = open(self.path + "high_score.txt", "w")
        for item in self.high_score:
            file.write(item[0] + ":" + str(item[1]) + "\n")
        file.close()

    def AddOptions(self, intro_text, screen):

        pixel_offset = 70
        for i in range(len(intro_text)):
            pos_x = (screen.get_size()[0] - self.font.size(intro_text[i])[0]) / 2
            pos_y = screen.get_size()[1] / 2 + (i * pixel_offset)
            self.options.append(Option(intro_text[i], (pos_x, pos_y), screen, self.font, RED, WHITE))

    def OnePlayer(self):
        block_number = 10
        subscreen_width = 500
        bottom_wall = self.board_height % (subscreen_width / block_number)
        p_ss = self.screen.subsurface(pygame.Rect(((self.board_width - subscreen_width) / 2), 0,
                                                  subscreen_width, self.board_height - bottom_wall))
        figure_prediction = p_ss.subsurface(pygame.Rect(0, 0, p_ss.get_size()[0] / 5, p_ss.get_size()[1] / 10))
        p = Player(self.clock, 1, self.logo, p_ss, figure_prediction, block_number)
        while self.run_game:
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    self.KeyDown(action[1], p)
            if p.CheckGameOver():
                p.GameOver()
                self.run_game = False
            else:
                p.move()
                p.SetOpponentSpeedControl(p.score)

            pygame.display.flip()
            self.screen.fill(GREY)
            p_ss.fill(BLACK)
            figure_prediction.fill(BLACK)
            self.clock.tick(FPS)
        if p.CheckIfHighScore(self.high_score):
            p.GetPlayerName(self.input_reader)
        self.SetHighScore(p)

    def TwoPlayer(self):
        block_number = 10
        subscreen_width = 500
        pos_x = (self.board_width - 2 * subscreen_width - WALL_SIZE) / 2
        bottom_wall = self.board_height % (subscreen_width / block_number)
        p1_ss = self.screen.subsurface(pygame.Rect(pos_x, 0, subscreen_width, self.board_height - bottom_wall))
        p2_ss = self.screen.subsurface(pygame.Rect(pos_x + subscreen_width + WALL_SIZE,
                                                   0, subscreen_width, self.board_height - bottom_wall))
        figure_prediction_1 = p1_ss.subsurface(pygame.Rect(0, 0, p1_ss.get_size()[0] / 5, p1_ss.get_size()[1] / 10))
        figure_prediction_2 = p2_ss.subsurface(pygame.Rect(0, 0, p2_ss.get_size()[0] / 5, p2_ss.get_size()[1] / 10))
        p1 = Player(self.clock, 1, self.logo, p1_ss, figure_prediction_1, block_number)
        p2 = Player(self.clock, 2, self.logo, p2_ss, figure_prediction_2, block_number)
        while self.run_game:
            for event in pygame.event.get():
                action = self.input_reader.readInput(event)
                if action is not None:
                    if action[0] == 0:
                        self.KeyDown(action[1], p1)
                    elif action[0] == 1:
                        self.KeyDown(action[1], p2)

            if p1.CheckGameOver():
                p1.GameOver()
            else:
                p1.move()
                if p2.CheckGameOver():
                    p1.SetOwnSpeedControl(p2.score)
                else:
                    p2.SetOpponentSpeedControl(p1.score)

            if p2.CheckGameOver():
                p2.GameOver()
            else:
                p2.move()
                if p1.CheckGameOver():
                    p2.SetOwnSpeedControl(p1.score)
                else:
                    p1.SetOpponentSpeedControl(p2.score)

            if p1.CheckGameOver() and p2.CheckGameOver():
                self.run_game = False

            pygame.display.flip()
            self.screen.fill(GREY)
            p1_ss.fill(BLACK)
            p2_ss.fill(BLACK)
            figure_prediction_1.fill(BLACK)
            figure_prediction_2.fill(BLACK)
            self.clock.tick(FPS)
        if p1.CheckIfHighScore(self.high_score):
            p1.GetPlayerName(self.input_reader)
        if p2.CheckIfHighScore(self.high_score):
            p2.GetPlayerName(self.input_reader)
        self.SetHighScore(p1, p2)


def RunTetris(screen):
    main = Main(screen)
    main.start()
    return