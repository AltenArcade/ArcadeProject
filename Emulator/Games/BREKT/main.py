from platform import system
from os import path
import pygame
import Games.BREKT.game as g
import Games.BREKT.classes as cl
import random as rn
import Games.BREKT.levels as lvl
from InputReader import InputReader


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.y_offset = int(self.height / 20)
        self.done = False

        # NEW ----------------------------------------------------------------------------------------------------------
        if system() == "Windows": 
            self.path = str(path.dirname(path.realpath(__file__))) + "\\"
        if system() == "Linux":
            self.path = str(path.dirname(path.realpath(__file__))) + "/"

        self.font = pygame.font.SysFont('Calibri', int(self.height / 15), True, False)
        self.font = pygame.font.Font(self.path + 'font.ttf', int(self.height / 22))
        self.high_score = self.get_high_score()
        self.block_list = pygame.sprite.Group()
        self.input_reader = InputReader()
        # --------------------------------------------------------------------------------------------------------------

        self.clock = pygame.time.Clock()

        # Initiate and draw constant background
        self.bg_screen = pygame.Surface([self.width, self.height])
        self.bg_screen.fill(cl.BLACK)
        for i in range(int(self.height / 2)):
            bg_pos_x = rn.random() * self.width
            bg_pos_y = rn.random() * self.height
            pygame.draw.line(self.bg_screen, cl.WHITE, [bg_pos_x, bg_pos_y], [bg_pos_x, bg_pos_y], 1)

        # NEW ----------------------------------------------------------------------------------------------------------
        # Initiate and draw constant background
        self.hs_block_list = pygame.sprite.Group()
        # --------------------------------------------------------------------------------------------------------------

        # NEW ----------------------------------------------------------------------------------------------------------
        #pygame.draw.rect(self.bg_screen, cl.GREY, [0, 0, self.width / 400, self.height])
        #pygame.draw.rect(self.bg_screen, cl.GREY, [self.width - self.width / 400, 0, self.width / 400, self.height])
        # --------------------------------------------------------------------------------------------------------------

        self.start_menu()

    def start_menu(self):
        sel = 0
        execute = [self.start_game, self.view_high_score, self.exit_game]
        self.block_list = self.init_menu_blocks(self.width, self.height, self.y_offset, lvl.menu_bp)
        self.hs_block_list = self.init_menu_blocks(self.width, self.height, self.y_offset, lvl.hs_bp)

        self.done = False
        while not self.done:
            # Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                else:
                    action = self.input_reader.readInput(event)
                    if action is not None and action[0] == 0:
                        action = action[1]
                        if action == "up":
                            if sel > 0:
                                sel -= 1
                            else:
                                sel = 2
                        elif action == "down":
                            if sel < 2:
                                sel += 1
                            else:
                                sel = 0
                        elif action == "execute":
                            execute[sel]()

            self.screen.blit(self.bg_screen, (0, 0))
            self.block_list.draw(self.screen)
            self.draw_menu(sel)
            pygame.display.flip()

            # Limit to 60 frames per second
            self.clock.tick(60)

    # NEW---------------------------------------------------------------------------------------------------------------
    def draw_menu(self, sel):
        menu_colors = [cl.YELLOW_DARK, cl.YELLOW_DARK, cl.YELLOW_DARK]
        menu_colors[sel] = cl.YELLOW

        #font_sel = pygame.font.SysFont('Calibri', int(self.height / 15.5), True, False)
        #font = pygame.font.SysFont('Calibri', int(self.height / 16.67), True, False)
        font_sel = pygame.font.Font(self.path + 'font.ttf', int(self.height / 20))
        font = pygame.font.Font(self.path + 'font.ttf', int(self.height / 24))
        menu_fonts = [font, font, font]
        menu_fonts[sel] = font_sel

        text_0 = menu_fonts[0].render("START GAME", True, menu_colors[0])
        text_1 = menu_fonts[1].render("HIGH SCORE", True, menu_colors[1])
        text_2 = menu_fonts[2].render("EXIT", True, menu_colors[2])

        self.screen.blit(text_0, [(self.width / 2) - text_0.get_rect().width / 2,
                                    ((4 * self.height) / 6) - self.height / 11])
        self.screen.blit(text_1, [(self.width / 2) - text_1.get_rect().width / 2, ((4 * self.height) / 6)])
        self.screen.blit(text_2, [(self.width / 2) - text_2.get_rect().width / 2,
                                    ((4 * self.height) / 6) + self.height / 11])
    # ------------------------------------------------------------------------------------------------------------------

    def init_menu_blocks(self, width, height, y_offset, bp_str):
        block_list = pygame.sprite.Group()
        bp = self.construct_bp(bp_str)
        block_w = width / len(bp[0])
        block_h = height / (len(bp[0]) * 1.5)
        for i in range(len(bp)):
            for j in range(len(bp[i])):
                if bp[i][j] != 0:
                    pos_x = block_w / 2 + j * block_w
                    pos_y = y_offset + block_h / 2 + i * block_h
                    b = cl.Block(bp[i][j], block_w - width / 400, block_h - height / 250, pos_x, pos_y)
                    block_list.add(b)
        return block_list

    def construct_bp(self, str):
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

    def high_score(self):
        print("high")

    def start_game(self):
        game = g.Game(self.screen, self.width, self.height, self.y_offset,
                      self.bg_screen, self.clock, self.high_score, self.hs_block_list)
        self.start_menu()

# NEW ------------------------------------------------------------------------------------------------------------------
    def get_high_score(self):
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
    def exit_game(self):
        self.done = True

    def view_high_score(self):
        self.high_score = self.get_high_score()
        self.show_high_score()
# ----------------------------------------------------------------------------------------------------------------------

def RunBrekt(screen):
    #pygame.init()
    #size = (1600, 1000)
    #pygame.screen = pygame.display.set_mode(size)
    #pygame.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    #pygame.display.set_caption("BREKT")

    pygame.mouse.set_visible(0)
    menu = Menu(screen)
