import pygame
from os import path
from os import environ
from tetris.Main import RunTetris
from Achtung.Achtung import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)
GREY = (160, 160, 160)

class MainGUI:
    def __init__(self, screen):
        self.state_idx = 0
        self.states = []
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.font = pygame.font.Font(path.abspath("font.ttf"), 20)
        self.board_width = self.screen.get_size()[0]
        self.board_height = self.screen.get_size()[1]
        self.screen.fill(WHITE)
        self.option_screen = self.screen.subsurface(0, self.board_height / 2, self.board_width, self.board_height / 2)
        self.options = []

    def Start(self):
        self.screen.fill(WHITE)
        ret_val = ""
        done = False
        idx = 0
        self.SetOptions("start")
        self.options[idx].hovered = True
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                        ret_val = "quit"
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
                        if self.options[idx].text == "Tetris":
                            ret_val = "tetris"
                            done = True
                        elif self.options[idx].text == "Snake":
                            ret_val = "Snake"
                            done = True
                        else:
                            idx = self.SetOptions(self.options[idx].text)
                            self.options[idx].hovered = True

            self.option_screen.fill(WHITE)
            for option in self.options:
                option.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return ret_val

    def SetOptions(self, case):
        self.options.clear()
        if case == "start":
            intro_text = ["Select Game", "Settings", "Exit"]
            self.DrawOptions(intro_text)
        elif case == "Select Game":
            intro_text = ["Tetris", "Pong", "Snake"]
            self.DrawOptions(intro_text)
        return 0

    def DrawOptions(self,intro_text):

        pixel_offset = 70
        logo = pygame.image.load(path.abspath("AltenArcadeLogo.png")).convert_alpha()
        logo = self.ScaleImage(logo, self.board_width)
        screen_center = (self.board_width - logo.get_size()[0])/ 2
        pos_y = (self.option_screen.get_size()[1] - (3 * self.font.size(intro_text[0])[1] + 2 * pixel_offset)) / 2
        for i in range(len(intro_text)):
            self.options.append(Option(intro_text[i],((self.board_width - self.font.size(intro_text[i])[0]) / 2,pos_y + (i * pixel_offset)),self.option_screen,self.font))
        self.screen.blit(logo, (screen_center, self.board_height * 0.1))

    def ScaleImage(self,img,width):
        img_ratio = img.get_rect().size[1] / img.get_rect().size[0]
        return pygame.transform.scale(img,(width,int(width * img_ratio)))

class Option:
    hovered = False

    def __init__(self, text, pos, screen, font):
        self.screen = screen
        self.font = font
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return RED
        else:
            return BLACK

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

class MainLoop:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,800))
        #self.screen = pygame.display.set_mode((1440, 900))
        environ['SDL_VIDEO_CENTERED'] = '1'

    def run(self):
        run = True
        main = MainGUI(self.screen)
        while run:
            ret = main.Start()
            if ret == "quit":
                run = False
            elif ret == "tetris":
                RunTetris(self.screen)
            elif ret == "Snake":
                AchtungMain(self.screen)

main = MainLoop()
main.run()
