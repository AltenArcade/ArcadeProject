import pygame
from pygame import joystick
from platform import system
from os import path
from Games.Tetris.Player import Player
from Option import Option

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
        self.board_height  = self.screen.get_size()[1]
        self.logo = pygame.image.load(self.path + "Estetris_logo.png").convert_alpha()
        self.logo = self.ScaleImage(self.logo, self.board_width)
        self.screen_center = (self.board_width - self.logo.get_size()[0]) / 2
        self.score = 0
        self.exit_game = False
        self.restart = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(self.path + "font.ttf", 20)
        self.high_score = []
        self.options = []
        pygame.mixer.music.load(self.path + "tetris-sound.mp3")
        self.background = pygame.image.load(self.path + "tetris_background.png")
        self.background = self.ScaleImage(self.background, self.board_width)

    def GetHighScore(self):
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

    def ScaleImage(self,img,width):

        img_ratio = img.get_rect().size[1] / img.get_rect().size[0]
        return pygame.transform.scale(img,(width,int(width * img_ratio)))

    def GetPlayers(self,logo,background,screen_center):
        done = False
        selection_font = pygame.font.Font(self.path + "font.ttf", 20)
        selection_font.set_underline(True)

        one_player = True
        start_string = "Players"
        text = self.font.render(start_string,1,WHITE)
        y_offset = 30
        x_offset = 20
        while not done:
            self.screen.blit(background, (0, self.board_height - background.get_height()))
            self.screen.blit(logo, (screen_center, 0))
            self.screen.blit(text, (( self.board_width - self.font.size(start_string)[0]) / 2, self.board_height * 0.4))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        one_player = False
                    if event.key == pygame.K_LEFT:
                        one_player = True
                    if event.key == pygame.K_RETURN:
                        done = True
                    if event.key == pygame.K_ESCAPE:
                        return 0
            txt_x = ( self.board_width - self.font.size("1")[0])/2
            if(one_player):
                self.screen.blit(selection_font.render("1",1,WHITE),(txt_x - x_offset,self.board_height * 0.4 + y_offset))
                self.screen.blit(self.font.render("2",1,WHITE), (txt_x + x_offset , self.board_height * 0.4 + y_offset))
            else:
                self.screen.blit(self.font.render("1",1,WHITE),(txt_x - x_offset, self.board_height * 0.4 + y_offset))
                self.screen.blit(selection_font.render("2",1,WHITE), (txt_x + x_offset, self.board_height * 0.4 + y_offset))

            pygame.display.flip()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

        if(one_player):
            return 1
        else:
            return 2

    def KeyDown(self, event, p1, p2 = 0):
        if event.key == pygame.K_ESCAPE:
            self.run_game = False
        elif event.key == pygame.K_UP:
            p1.flip()
        elif event.key == pygame.K_LEFT:
            p1.left()
        elif event.key == pygame.K_RIGHT:
            p1.right()
        elif event.key == pygame.K_DOWN:
            p1.down()
        elif event.key == pygame.K_RETURN:
            p1.down_fast()
        if p2 != 0:
            if event.key == pygame.K_w:
                p2.flip()
            elif event.key == pygame.K_a:
                p2.left()
            elif event.key == pygame.K_d:
                p2.right()
            elif event.key == pygame.K_s:
                p2.down()

    def insert_score(self,high_score, player):
        for i in range(len(high_score)):
            if high_score[i][1] < player.score:
                high_score.insert(i, [player.name, player.score])
                break
        high_score = sorted(high_score, key=lambda score: score[1])[::-1]
        while len(high_score) > 5:
            high_score.remove(high_score[len(high_score) - 1])
        return high_score

    def SetHighScore(self,player1, player2=0):
        if player2 == 0:
            self.high_score = self.insert_score(self.high_score, player1)
        else:
            if player1.score < player2.score:
                self.high_score = self.insert_score(self.high_score, player1)
                self.high_score = self.insert_score(self.high_score, player2)
            elif player1.score >= player2.score:
                self.high_score = self.insert_score(self.high_score, player2)
                self.high_score = self.insert_score(self.high_score, player1)
        return self.high_score

    def ShowHighScore(self):
        pixel_offset = 40
        i = 0
        self.screen.blit(self.background, (0, self.board_height - self.background.get_height()))
        self.screen.blit(self.logo, (self.screen_center, 0))
        for score in self.high_score:
            string = score[0] + " " + str(score[1])
            txt = self.font.render(string, 1, WHITE)
            self.screen.blit(txt, ((self.board_width - self.font.size(string)[0]) / 2,self.board_height * 0.4 + (i * pixel_offset)))
            i += 1
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return

    def SaveScore(self):
        file = open(self.path + "/high_score.txt", "w")
        for item in self.high_score:
            file.write(item[0] + ":" + str(item[1]) + "\n")
        file.close()

    def SetOptions(self, case):
        self.options.clear()
        if case == "Start":
            intro_text = ["New Game", "High Score", "Exit"]
            self.AddOptions(intro_text)
        return 0

    def AddOptions(self, intro_text):

        pixel_offset = 70
        for i in range(len(intro_text)):
            self.options.append(Option(intro_text[i],((self.board_width - self.font.size(intro_text[i])[0]) / 2,self.board_height * 0.35 + (i * pixel_offset)),self.screen,self.font, RED, WHITE))

    def start(self):
        self.high_score = self.GetHighScore()
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("Tetris")
        self.exit_game = False
        players = 0
        idx = 0
        self.SetOptions("Start")
        self.options[idx].hovered = True
        while not self.exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game = True
                    elif event.key == pygame.K_DOWN:
                        self.options[idx].hovered = False
                        idx += 1
                        if idx > 2:
                            idx = 0
                        self.options[idx].hovered = True
                    elif event.key == pygame.K_UP:
                        self.options[idx].hovered = False
                        idx -= 1
                        if idx < 0:
                            idx = len(self.options) - 1
                        self.options[idx].hovered = True
                    elif event.key == pygame.K_RETURN:
                        if self.options[idx].text == "High Score":
                            self.ShowHighScore()
                        elif self.options[idx].text == "Exit":
                            self.exit_game = True
                        elif self.options[idx].text == "New Game":
                            players = self.GetPlayers(self.logo, self.background, self.screen_center)
                            self.run_game = True

            if(self.run_game and players > 0):
                if players == 2:
                    self.TwoPlayer()
                else:
                    self.OnePlayer()
                self.SaveScore()
            self.screen.blit(self.background, (0, self.board_height - self.background.get_height()))
            self.screen.blit(self.logo, (self.screen_center, 0))
            for option in self.options:
                option.draw()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
        pygame.mixer.music.stop()
        return

    def OnePlayer(self):
        block_number = 10
        subscreen_width = 400
        p_ss = self.screen.subsurface(pygame.Rect(((self.board_width - subscreen_width) / 2), 0, subscreen_width, self.board_height))
        figure_prediction = p_ss.subsurface(pygame.Rect(0,0,p_ss.get_size()[0] / 5, p_ss.get_size()[1] / 10))
        p = Player(self.clock, 1, self.logo, p_ss, figure_prediction, block_number)
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False
                    self.exit_game = True
                elif event.type == pygame.KEYDOWN:
                    self.KeyDown(event, p)

            if p.CheckGameOver():
                p.GameOver()
                self.run_game = False
            else:
                p.move()

            pygame.display.flip()
            self.screen.fill(GREY)
            p_ss.fill(BLACK)
            figure_prediction.fill(BLACK)
            self.clock.tick(FPS)
        if p.CheckIfHighScore(self.high_score):
            p.GetPlayerName()
        self.SetHighScore(p)

    def TwoPlayer(self):
        block_number = 10
        subscreen_width = 400
        pos_x = (self.board_width - 2 * subscreen_width - WALL_SIZE) / 2
        bottom_wall = self.board_height % (subscreen_width / block_number)
        p1_ss = self.screen.subsurface(pygame.Rect(pos_x, 0, subscreen_width, self.board_height - bottom_wall))
        p2_ss = self.screen.subsurface(pygame.Rect(pos_x + subscreen_width + WALL_SIZE, 0, subscreen_width, self.board_height - bottom_wall))
        figure_prediction_1 = p1_ss.subsurface(pygame.Rect(0, 0, p1_ss.get_size()[0] / 5, p1_ss.get_size()[1] / 10))
        figure_prediction_2 = p2_ss.subsurface(pygame.Rect(0, 0, p2_ss.get_size()[0] / 5, p2_ss.get_size()[1] / 10))
        p1 = Player(self.clock, 1, self.logo, p1_ss, figure_prediction_1, block_number)
        p2 = Player(self.clock, 2, self.logo, p2_ss, figure_prediction_2, block_number)
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False
                    self.exit_game = True
                elif event.type == pygame.KEYDOWN:
                    self.KeyDown(event, p1, p2)

            if p1.CheckGameOver():
                p1.GameOver()
            else:
                p1.move()

            if p2.CheckGameOver():
                p2.GameOver()
            else:
                p2.move()
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
            p1.GetPlayerName()
        if p2.CheckIfHighScore(self.high_score):
            p2.GetPlayerName()
        self.SetHighScore(p1, p2)

def RunTetris(screen):
    main = Main(screen)
    main.start()
    return