from os import environ
from os import path
from platform import system
from Games.SNEK.Achtung import *
from Games.Tetris.Main import RunTetris
from Games.BREKT.main import RunBrekt
from Option import Option
from InputReader import InputReader
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 0, 142)
PURPLE = (182, 0, 251)
YELLOW = (251, 247, 5)
GREY = (160, 160, 160)

# This is the emulator class, working as a wrapper application for the games.


class MainGUI:

    def __init__(self, screen):
        if system() == "Windows":
            self.path = str(path.dirname(path.realpath(__file__))) + "\\"
        if system() == "Linux":
            self.path = str(path.dirname(path.realpath(__file__))) + "/"
        pygame.mouse.set_visible(False)
        self.screen = screen
        self.font = pygame.font.Font(self.path + "font.ttf", 30)
        self.board_width = self.screen.get_size()[0]
        self.board_height = self.screen.get_size()[1]
        self.screen.fill(WHITE)
        self.option_screen = self.screen.subsurface(0, self.board_height / 2, self.board_width, self.board_height / 2)
        self.options = []
        self.menu_length = 3
        self.current_options = [0, self.menu_length]
        self.current_source = []
        self.logo = pygame.image.load(self.path + "AltenArcadeLogo.png").convert_alpha()
        self.logo = self.ScaleImage(self.logo, self.board_width)

    # Get the game names by parsing the folder names inside the Games folder
    def GetDirs(self):
        ret = []
        game_path = ""
        if system() == "Windows":
            game_path = self.path + "Games" + "\\"
        elif system() == "Linux":
            game_path = self.path + "Games" + "/"
        for name in os.listdir(self.path + "Games"):
            if path.isdir(game_path + name):
                ret.append(name)
        return ret

    # Main game loop. Listens for keyboard or joystick events and execute desired game
    def Start(self):
        input_reader = InputReader()
        games = self.GetDirs()
        self.screen.fill(WHITE)
        clock = pygame.time.Clock()
        ret_val = ""
        done = False
        idx = 0
        self.current_source = ["Select Game", "Settings", "Exit"]
        idx = self.SetOptions(idx, True)
        while not done:
            for event in pygame.event.get():
                action = input_reader.readInput(event)
                if action is not None:
                    action = action[1]
                    if action == 'back':
                        self.current_options = [0, self.menu_length]
                        done = True
                    elif action == 'down':
                        self.options[idx].hovered = False
                        idx += 1
                        idx = self.SetOptions(idx)
                    elif action == 'up':
                        self.options[idx].hovered = False
                        idx -= 1
                        idx = self.SetOptions(idx)
                    elif action == 'execute':
                        if self.options[idx].text in games:
                            ret_val = self.options[idx].text
                            done = True
                        elif self.options[idx].text == "Exit":
                            done = True
                            ret_val = "quit"
                        elif self.options[idx].text == "Settings":
                            settings = Settings(self.option_screen, self.font)
                            settings.show()
                        else:
                            self.current_source = games
                            idx = self.SetOptions(idx, True)

            self.option_screen.fill(WHITE)
            for option in self.options:
                option.draw()

            # If there are more than 3 games the menu should only display
            # 3 games at a time and display an arrow up or down
            # depending on where to scroll for more games

            if self.current_options[0] > 0:
                pygame.draw.polygon(self.option_screen, BLACK, [
                    [self.board_width / 2 - 10, self.options[0].rect.y - 30],
                    [self.board_width / 2 + 10, self.options[0].rect.y - 30],
                    [self.board_width / 2, self.options[0].rect.y - 50]])
            if self.current_options[1] < len(self.current_source):
                pygame.draw.polygon(self.option_screen, BLACK, [
                    [self.board_width / 2 - 10, self.options[-1].rect.y + self.options[-1].rect.height + 30],
                    [self.board_width / 2 + 10, self.options[-1].rect.y + self.options[-1].rect.height + 30],
                    [self.board_width / 2, self.options[-1].rect.y + self.options[-1].rect.height + 50]])
            pygame.display.flip()
            clock.tick(60)
        return ret_val

    # Select which option to hover
    def SetOptions(self, idx, init=False):

        if idx >= self.menu_length:
            if len(self.current_source) > self.current_options[1]:
                self.options.clear()
                for i in range(len(self.current_options)):
                    self.current_options[i] += 1
                self.DrawOptions(self.current_source[self.current_options[0]:self.current_options[1]])
            idx = self.menu_length - 1
        elif idx < 0:
            if self.current_options[0] > 0:
                self.options.clear()
                for i in range(len(self.current_options)):
                    self.current_options[i] -= 1
                self.DrawOptions(self.current_source[self.current_options[0]:self.current_options[1]])
            idx = 0
        elif init:
            self.options.clear()
            self.DrawOptions(self.current_source[self.current_options[0]:self.current_options[1]])
            idx = 0
        self.options[idx].hovered = True
        return idx

    def DrawOptions(self, intro_text):

        pixel_offset = 70
        screen_center = (self.board_width - self.logo.get_size()[0]) / 2
        pos_y = (self.option_screen.get_size()[1] - (3 * self.font.size(intro_text[0])[1] + 2 * pixel_offset)) / 2
        for i in range(len(intro_text)):
            pos = ((self.board_width - self.font.size(intro_text[i])[0]) / 2, pos_y + (i * pixel_offset))
            self.options.append(Option(intro_text[i], pos, self.option_screen, self.font, RED, BLACK))
        self.screen.blit(self.logo, (screen_center, self.board_height * 0.1))

    def ScaleImage(self, img, width):
        img_ratio = img.get_rect().size[1] / img.get_rect().size[0]
        return pygame.transform.scale(img, (width, int(width * img_ratio)))

# A class for adding settings to the Arcade machine. No settings are currently implemented.


class Settings:

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.width = self.screen.get_size()[0]
        self.height = self.screen.get_size()[1]

    def show(self):
        done = False
        y_offset = 70
        text = ["Nothing here yet!", "Press any key..."]
        reader = InputReader()
        while not done:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                action = reader.readInput(event)
                if action is not None:
                    done = True
            for i in range(len(text)):
                posx = (self.width - self.font.size(text[i])[0]) / 2
                posy = (self.height - len(text) * self.font.size(text[i])[1]) / 2 + (i * y_offset)
                txt = self.font.render(text[i], 1, BLACK)
                self.screen.blit(txt, (posx, posy))
            pygame.display.flip()

# The main class creating a fullscreen pygame.Surface object and displays the MainGUI.
# When the user selects a game the same Surface object gets passed to the game
# and the graphics is displayed on this object.


class MainLoop:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), FULLSCREEN)

        # Force the screen ratio to 16:10 to match the arcade machine screen
        if self.screen.get_width() / self.screen.get_height() != 1.6:
            self.screen = pygame.display.set_mode([1280, 800])
        environ['SDL_VIDEO_CENTERED'] = '1'

    def run(self):
        run = True
        emulator_main = MainGUI(self.screen)
        while run:
            ret = emulator_main.Start()
            if ret == "quit":
                run = False
            elif ret == "Tetris":
                RunTetris(self.screen)
            elif ret == "SNEK":
                AchtungMain(self.screen)
            elif ret == "BREKT":
                RunBrekt(self.screen)


main = MainLoop()
main.run()