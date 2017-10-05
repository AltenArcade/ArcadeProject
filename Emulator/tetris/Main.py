import pygame
from os import path
from tetris.Player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)
GREY = (160, 160, 160)

FPS = 60

class Main:

    def __init__(self, screen):
        #pygame.init()
        self.run_game = False
        self.screen = screen
        self.board_width = self.screen.get_size()[0]
        self.board_height  = self.screen.get_size()[1]
        self.score = 0
        self.exit_game = False
        self.restart = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(path.abspath("font.ttf"), 20)
        self.high_score = self.GetHighScore()

        pygame.mixer.music.load(path.abspath("tetris\\tetris-sound.mp3"))
        self.background = pygame.image.load(path.abspath("tetris\\tetris_background.png"))
        self.background = self.ScaleImage(self.background, self.board_width)
        self.logo = pygame.image.load(path.abspath("tetris\\Estetris_logo.png")).convert_alpha()
        self.logo = self.ScaleImage(self.logo, self.board_width)
        
    def GetHighScore(self):
        file = open("tetris\\high_score.txt", "r")
        lst = [l.split() for l in file.readlines()]
        for t in lst:
            try:
                t[1] = int(t[1])
            except ValueError:
                print("Error can not be integer")
        s = sorted(lst, key=lambda score: score[1])[::-1]
        return s

    def SetIntroScreen(self, logo, screen_center):

        pixel_offset = 70
        intro_text = ["New Game: RCTRL", "Exit: ESC", "High Score: ENTER"]
        for i in range(len(intro_text)):
            txt = self.font.render(intro_text[i], 1, WHITE)
            self.screen.blit(txt, ((self.board_width - self.font.size(intro_text[i])[0]) / 2,self.board_height * 0.35 + (i * pixel_offset)))
        self.screen.blit(logo, (screen_center, self.board_height * 0.1))

    def ScaleImage(self,img,width):

        img_ratio = img.get_rect().size[1] / img.get_rect().size[0]
        return pygame.transform.scale(img,(width,int(width * img_ratio)))

    def GetPlayers(self,logo,background,screen_center):
        done = False
        selection_font = pygame.font.Font(path.abspath("font.ttf"), 20)
        selection_font.set_underline(True)

        one_player = True
        start_string = "Players"
        text = self.font.render(start_string,1,WHITE)
        y_offset = 30
        x_offset = 20
        while not done:
            self.screen.blit(background, (0, self.board_height - background.get_height()))
            self.screen.blit(logo, (screen_center, self.board_height * 0.1))
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
            self.board_width = 1000
            self.screen = pygame.display.set_mode((self.board_width, self.board_height))
            return 1
        else:
            self.board_width = 1010
            self.screen = pygame.display.set_mode((self.board_width, self.board_height))
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


    def ShowHighScore(self, logo, screen_center):
        pixel_offset = 40
        i = 0
        for score in self.high_score:
            string = score[0] + " " + str(score[1])
            txt = self.font.render(string, 1, WHITE)
            self.screen.blit(txt, ((self.board_width - self.font.size(string)[0]) / 2,self.board_height * 0.4 + (i * pixel_offset)))
            i += 1
        self.screen.blit(logo, (screen_center, self.board_height * 0.1))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return

    def SaveScore(self):
        file = open("high_score.txt", "w")
        for item in self.high_score:
            file.write(item[0] + " " + str(item[1]) + "\n")



    def start(self):
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("Tetris")
        screen_center = (self.board_width - self.logo.get_size()[0])/ 2
        self.exit_game = False
        players = 0
        while not self.exit_game:

            self.screen.blit(self.background, (0, self.board_height - self.background.get_height()))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game = True
                    if event.key == pygame.K_RETURN:
                        self.ShowHighScore(self.logo,screen_center)
                    if event.key == pygame.K_RCTRL:
                        players = self.GetPlayers(self.logo,self.background,screen_center)
                        self.run_game = True

            self.SetIntroScreen(self.logo,screen_center)
            if(self.run_game and players > 0):
                p1_ss = self.screen.subsurface(pygame.Rect((self.board_width / 2) + 5,0,(self.board_width / 2) - 5,self.board_height))
                p2_ss = self.screen.subsurface(pygame.Rect(0,0,(self.board_width / 2) - 5,self.board_height))
                if players == 2:
                    block_number = 10
                    p1 = Player(self.clock,1,self.logo,p1_ss, block_number)
                    p2 = Player(self.clock,2,self.logo,p2_ss, block_number)
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
                        self.clock.tick(FPS)
                    if p1.CheckIfHighScore(self.high_score):
                        p1.GetPlayerName()
                    if p2.CheckIfHighScore(self.high_score):
                        p2.GetPlayerName()
                    self.SetHighScore(p1,p2)
                else:
                    block_number = 20
                    p = Player(self.clock,1,self.logo,self.screen, block_number)
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
                        self.screen.fill(BLACK)
                        self.clock.tick(FPS)
                    if p.CheckIfHighScore(self.high_score):
                        p.GetPlayerName()
                    self.SetHighScore(p)
                self.SaveScore()
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.clock.tick(FPS)

        return

class RunTetris:
    def __init__(self, screen):
        self.main = Main(screen)

    def run_tetris(self):
        self.main.start()
        return