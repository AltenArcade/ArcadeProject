import pygame
from pygame.locals import *
from platform import system

BLUE = (51, 51, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255, 51, 51)
PINK = (255, 0, 255)

class Snake(pygame.sprite.Sprite):
    '''
    Playable snake that responds to key input.
    '''

    def __init__(self, x, y, color, size, direction):
        pygame.sprite.Sprite.__init__(self)
        self.width = size
        self.height = size
        self.color = color

        # Head
        self.image = pygame.Surface((self.width, self.height))#pygame.image.load('snake.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(self.color)

        # Tail
        self.tailImage = []
        self.tailRect = []

        self.length = 3
        self.pellets = 0
        self.score = 0
        self.score_tick = 0
        self.x_dist = self.width
        self.y_dist = self.height
        self.current_dir = direction
        self.speed = 1
        self.next_move = pygame.Rect(self.rect.x + self.width, self.rect.y, self.width, self.height)
        self.banned_move = None
        self.stunned = 0
        self.stun_time = 10
        self.key_registered = False

        for i in range(self.length):
            self.tailImage.append(pygame.Surface((self.width, self.height)))
            self.tailRect.append(self.tailImage[-1].get_rect())


    def move(self):
        xMove = 0
        yMove = 0

        if(self.stunned == 0):

            # Update movement of tail
            for i in range(len(self.tailRect)-1, -1, -1):
                if(i == 0):
                    self.tailRect[i].x = self.rect.x
                    self.tailRect[i].y = self.rect.y
                else:
                    self.tailRect[i].x = self.tailRect[i-1].x
                    self.tailRect[i].y = self.tailRect[i-1].y

            # Update movement of head
            if(self.current_dir == 'right' and self.banned_move != 'right'):
                xMove = self.x_dist
            elif(self.current_dir == 'left' and self.banned_move != 'left'):
                xMove = -self.x_dist
            elif(self.current_dir == 'up' and self.banned_move != 'up'):
                yMove = -self.y_dist
            elif(self.current_dir == 'down' and self.banned_move != 'down'):
                yMove = self.y_dist

            self.rect.move_ip(xMove, yMove)
        else:
            self.stunned -= 1

    def updateNextMove(self):
        if (self.current_dir == 'left'):
            self.next_move.x = self.rect.x - self.width
            self.next_move.y = self.rect.y
        elif (self.current_dir == 'right'):
            self.next_move.x = self.rect.x + self.width
            self.next_move.y = self.rect.y
        elif (self.current_dir == 'up'):
            self.next_move.x = self.rect.x
            self.next_move.y = self.rect.y - self.height
        elif (self.current_dir == 'down'):
            self.next_move.x = self.rect.x
            self.next_move.y = self.rect.y + self.height


    def setDirection(self, key):

        if (key != None):
            if ((key == K_RIGHT or key == K_d or key == 'right') and self.banned_move != 'right' and self.current_dir != 'left'):
                self.current_dir = 'right'
                self.next_move.x = self.rect.x + self.width
                self.next_move.y = self.rect.y
            elif ((key == K_LEFT or key == K_a or key == 'left') and self.banned_move != 'left' and self.current_dir != 'right'):
                self.current_dir = 'left'
                self.next_move.x = self.rect.x - self.width
                self.next_move.y = self.rect.y
            elif ((key == K_UP or key == K_w or key == 'up') and self.banned_move != 'up' and self.current_dir != 'down'):
                self.current_dir = 'up'
                self.next_move.x = self.rect.x
                self.next_move.y = self.rect.y - self.height
            elif ((key == K_DOWN or key == K_s or key == 'down') and self.banned_move != 'down' and self.current_dir != 'up'):
                self.current_dir = 'down'
                self.next_move.x = self.rect.x
                self.next_move.y = self.rect.y + self.height

    def checkTailCollision(self):
        return self.rect.collidelist(self.tailRect) != -1

    def checkSnakeCollision(self, snake):
        return self.next_move.collidelist(snake.tailRect) != -1

    def checkWallCollision(self, walls):
        self.banned_move = None
        wallCols = self.next_move.collidelist(walls)

        if (wallCols != -1):
            if (wallCols == 0):
                self.banned_move = 'left'
            elif (wallCols == 2):
                self.banned_move = 'right'
            elif (wallCols == 1):
                self.banned_move = 'up'
            elif (wallCols == 3):
                self.banned_move = 'down'

    def checkPelletCollision(self, pellets):
        pelletCols = pygame.sprite.spritecollide(self, pellets, True)
        return len(pelletCols) == 1

    def increasePelletCount(self):
        self.pellets += 1

    def grow(self):
        self.length += 1
        self.tailImage.append(pygame.Surface((self.width, self.height)))
        self.tailRect.append(self.tailImage[-1].get_rect())
        self.score += 10

class Pellet(pygame.sprite.Sprite):
    '''
    Pellet that the snake(s) can pick up.
    '''

    def __init__(self, x, y, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height


class Wall(pygame.sprite.Sprite):
    '''
    Walls defining the game area.
    '''

    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class DJ():
    '''
    Class for playing music and sound effects.
    '''

    def __init__(self, path):

        # Define music songs
        self.path = path
        self.introMusic = self.path + 'right_back_into_you.mp3'
        self.gameOverMusic = self.path + 'game_over_loop.mp3'
        self.onePlayerMusic = self.path + 'cosmic.mp3'
        self.twoPlayerMusic = self.path + 'twoplayer.mp3'

        # Define sound effects
        self.gameOverSound = pygame.mixer.Sound(self.path + 'game_over2.wav')
        self.collisionSound = pygame.mixer.Sound(self.path + 'explosion.wav')
        self.pickUpSound = pygame.mixer.Sound(self.path + 'collision.wav')

    def playIntroMusic(self):
        pygame.mixer.music.load(self.introMusic)
        pygame.mixer.music.play(-1)

    def playGameMusic(self, numberOfPlayers):
        if(numberOfPlayers == 1):
            pygame.mixer.music.load(self.onePlayerMusic)
        elif(numberOfPlayers == 2):
            pygame.mixer.music.load(self.twoPlayerMusic)

        pygame.mixer.music.play(-1)

    def playGameOverMusic(self):
        self.gameOverSound.play()
        pygame.mixer.music.load(self.gameOverMusic)
        pygame.mixer.music.play(-1)

    def playPickUpSound(self):
        self.pickUpSound.play()

    def playCollisionSound(self):
        self.collisionSound.play()

    def stopMusic(self):
        pygame.mixer.music.stop()

class Painter:
    '''
    Renders everything onto a screen.
    '''

    def __init__(self, screen_size, score_margin, img_path, font_path):
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.img_path = img_path
        self.font_path = font_path
        self.score_margin = score_margin
        self.font = pygame.font.Font(None, 46)
        self.font2 = pygame.font.SysFont('monospace', 16)
        self.font3 = pygame.font.SysFont('monospace', 20)
        self.versionFont = pygame.font.SysFont('monospace', 16)
        if system() == "Windows":
            font_extension = '.ttf'
        if system() == "Linux":
            font_extension = '.TTF'
        self.arcadeFont = pygame.font.Font(self.font_path + 'ARCADE_I' + font_extension, 22)
        self.arcadeFontSmall = pygame.font.Font(self.font_path + 'ARCADE_I' + font_extension, 18)
        self.arcadeFontNormal = pygame.font.Font(self.font_path + 'ARCADE_N' + font_extension, 16)
        self.arcadeFontMedium = pygame.font.Font(self.font_path + 'ARCADE_N' + font_extension, 18)

        # Start screen
        self.startMenuTextColor = BLUE
        self.selectSquare = pygame.Surface((220, 30))
        self.selectSquareStartGame = pygame.Surface((50, 30))
        logoImage = pygame.image.load(self.img_path + 'SNEK_logo1_r.png')
        ratio = logoImage.get_width() / logoImage.get_height()
        self.logoImage = pygame.transform.scale(logoImage,
                                                (round(self.screen_width / 3), round(self.screen_width / 3 / ratio)))
        self.logoImageSmall = pygame.transform.scale(logoImage,
                                                (round((self.score_margin - 2) * ratio), round(self.score_margin - 2)))
        self.startGameText = self.arcadeFont.render('Start game', True, self.startMenuTextColor)
        self.optionsText = self.arcadeFont.render('Highscore', True, self.startMenuTextColor)
        self.quitText = self.arcadeFont.render('Quit', True, self.startMenuTextColor)
        self.versionText = self.versionFont.render('Version ' + str(0.1), True, RED)
        self.onePlayerText = self.arcadeFont.render('1P', True, self.startMenuTextColor)
        self.twoPlayerText = self.arcadeFont.render('2P', True, self.startMenuTextColor)

        # Game over screen
        fontColor = BLACK
        self.retryText = self.arcadeFont.render('Play again?', True, fontColor)
        self.yesText = self.arcadeFont.render('Yes', True, fontColor)
        self.noText = self.arcadeFont.render('No', True, fontColor)
        gameOverImage = pygame.image.load(self.img_path + 'erik400.png')
        self.gameOverImage = pygame.transform.scale(gameOverImage, (round(self.screen_width / 3), round(self.screen_height / 2.2)))
        self.selectSquareGameOver = pygame.Surface((60, 30))

        self.wall_color = BLACK
        self.background_color = YELLOW
        self.snake_colors = [RED, BLUE]
        self.pellet_color = BLUE
        self.neutral_color = BLACK
        self.highscoreWindowColor = BLUE
        self.highscoreFontColor = WHITE

        self.draw_next_move = False

    def drawNextMove(self, screen, snake):
        pygame.draw.rect(screen, [0, 255, 0], snake.next_move)

    #def drawPromptBox(self):

    def drawStartScreen(self, screen, start_game, selectable_positions, selectable_position_index, selectable_positions_start_game, selectable_position_index_start_game):
        '''
        Draws the start screen on given screen surface.
        :param screen: The screen onto which rendering is done.
        :param start_game: True/False if start game menu is triggered.
        :param selectable_positions:
        :param selectable_position_index:
        :param selectable_positions_start_game:
        :param selectable_position_index_start_game:
        :return: None
        '''

        screen.fill(YELLOW)
        self.drawSurface(screen, self.versionText, 2)
        self.drawSurface(screen, self.startGameText, 4)
        self.drawSurface(screen, self.optionsText, 5)
        self.drawSurface(screen, self.quitText, 6)
        self.drawSurface(screen, self.logoImage, 1)

        if (start_game):
            self.drawSurface(screen, self.onePlayerText, 9)
            self.drawSurface(screen, self.twoPlayerText, 10)
            self.drawSurface(screen, self.selectSquareStartGame, 17, 128, selectable_positions_start_game[selectable_position_index_start_game],
                             self.startMenuTextColor)
        else:
            self.drawSurface(screen, self.selectSquare, 13, 128, selectable_positions[selectable_position_index], self.startMenuTextColor)

        pygame.display.flip()


    def drawGameObjects(self, screen, sprite_list, snakes, score_window, current_highscore):
        
        # Draw background
        screen.fill(self.background_color)
        
        # Draw sprites (snake heads, pellets and walls)
        for n in range(len(sprite_list)):
            sprite_list[n].draw(screen)

        # Draw snake tails
        for snake in range(len(snakes)):
            for i in range(len(snakes[snake].tailRect), -1, -1):
                pygame.draw.rect(screen, snakes[snake].color, snakes[snake].tailRect[i - 1])

        # Score window
        score_window.fill(self.background_color)

        # Draw score
        for snake in range(len(snakes)):
            scoretext = self.arcadeFontMedium.render("Score: {0}".format(snakes[snake].score), 1,
                                                     snakes[snake].color)
            score_window.blit(scoretext, (5 + snake * (score_window.get_width() - scoretext.get_rect().width - 10), 10))

        # Draw SNEK logo
        score_window.blit(self.logoImageSmall, (self.screen_width / 2 - self.logoImageSmall.get_width() / 2, self.score_margin / 2 - self.logoImageSmall.get_height() / 2))

        # Draw highscore (single player)
        if (len(snakes) == 1):
            highScoreText = self.arcadeFontMedium.render('Highscore: {0}'.format(current_highscore[1]), 1,
                                                         BLUE)
            highScoreText2 = self.arcadeFontMedium.render('Set by: {0}'.format(current_highscore[0]), 1,
                                                          BLUE)
            highScoreText_rect = highScoreText.get_rect()
            highScoreText2_rect = highScoreText2.get_rect()
            score_window.blit(highScoreText, (score_window.get_width() - highScoreText_rect.width - 10, 10))
            score_window.blit(highScoreText2,
                             (score_window.get_width() - highScoreText2_rect.width - 10, 10 + highScoreText_rect.height))

        # Draw score window
        screen.blit(score_window, (0, 0))


    def drawGameOverScreen(self, screen, selectable_positions, selectable_pos_index, font_color, winner = None):

        '''
        Draws the game over screen on given screen surface.
        :param screen: The screen onto which rendering is done.
        :param selectable_positions: Available logical positions for selecting square.
        :param selectable_pos_index: Index for available logical positions.
        :param font_color: Color for menu text.
        :param winner: Winning snake (1 or 2)
        :param winner_text: Winning text.
        :return: None
        '''

        self.drawSurface(screen, self.retryText, 5)
        self.drawSurface(screen, self.yesText, 15)
        self.drawSurface(screen, self.noText, 16)
        self.drawSurface(screen, self.gameOverImage, 0)
        if (winner != None):
            winner_text = self.arcadeFontNormal.render('Player ' + str(winner) + ' wins!', True, font_color)
            self.drawSurface(screen, winner_text, 18 + (winner - 1) * 2)
        self.drawSurface(screen, self.selectSquareGameOver, 15, 128, selectable_positions[selectable_pos_index], BLACK)#font_color)
        pygame.display.flip()

    def drawHighscoreWindow(self, screen, window_size, top10):

        # Create highscore window and render text
        window_width = window_size[0]
        window_height = window_size[1]
        box = pygame.Surface((window_size[0], window_size[1]))
        box.fill(self.highscoreWindowColor)
        pygame.draw.rect(box, BLACK, (0, 0, window_width, window_height), 1)
        txt_surf = self.arcadeFont.render("HIGHSCORE", True, self.highscoreFontColor)
        txt_rect = txt_surf.get_rect(center = (window_width// 2, round(0.075 * window_height)))
        txt_height = txt_rect.y
        box.blit(txt_surf, txt_rect)
        txt_surf = self.arcadeFontSmall.render("Press ENTER to continue", True, self.highscoreFontColor)
        txt_rect = txt_surf.get_rect(center = (window_width// 2, window_height - round(0.075 * window_height)))
        box.blit(txt_surf, txt_rect)
        entry_spacing = (window_height - 4 * round(0.075 * window_height)) / 10

        # Render top 10
        for i, entry in enumerate(top10):
            txt_surf = self.arcadeFontNormal.render(entry[1] + "  " + str(entry[0]), True, self.highscoreFontColor)
            txt_rect = txt_surf.get_rect(
                center = (window_width // 2, entry_spacing * i + 2 * round(0.075 * window_height) + txt_height))
            box.blit(txt_surf, txt_rect)

        # Render the high score window
        screen.blit(box, (screen.get_width() / 2 - window_width / 2, screen.get_height() / 2 - window_height / 2))
        pygame.display.flip()

    def drawSurface(self, screen, surface, screenPos, alpha = None, tempPos = None, color = None):

        """ Draws a surface at defined logical screen position """

        columnWidth = round(screen.get_size()[0] / 4)
        rowHeight = round(screen.get_size()[1] / 10)
        surface_x = 0
        surface_y = 0
        surface_rect = surface.get_rect()
        logoMargin = 20

        # Check for screen positions

        # Version text
        if(screenPos == 0):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = screen.get_height() / 2 - surface_rect.height / 2
        # Game logo
        if(screenPos == 1):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = 2*rowHeight
        # Version text
        if(screenPos == 2):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = screen.get_height() / 2 + surface_rect.height
        # Menu position 2
        if(screenPos == 4):
            surface_x = 2*columnWidth - surface_rect.width / 2
            surface_y = 6*rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Menu position 3
        if(screenPos == 5):
            surface_x = 2*columnWidth - surface_rect.width / 2
            surface_y = 7*rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Menu position 4
        if(screenPos == 6):
            surface_x = 2*columnWidth - surface_rect.width / 2
            surface_y = 8*rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Menu position 5
        if(screenPos == 7):
            surface_x = 2 * columnWidth - surface_rect.width / 2
            surface_y = 9 * rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 9):
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2 - columnWidth / 2
            surface_y = 6*rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 10):
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2 - columnWidth / 2
            surface_y = 7*rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Select rectangle
        if(screenPos == 13 and tempPos != None):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = (2 + tempPos) * rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Alten logo (top right corner)
        if(screenPos == 14):
            surface_x = screen.get_width() - logoMargin - surface_rect.width
            surface_y = logoMargin
        # Menu position 5a
        if(screenPos == 15):
            if(tempPos != None):
                tempPos = tempPos - 14
                surface_x = tempPos * columnWidth + columnWidth / 2 - surface_rect.width / 2
                surface_y = 8 * rowHeight + rowHeight / 2 - surface_rect.height / 2
            else:
                surface_x = columnWidth + columnWidth / 2 - surface_rect.width / 2
                surface_y = 8 * rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Menu position 5b
        if(screenPos == 16):
            surface_x = 2 * columnWidth + columnWidth / 2 - surface_rect.width / 2
            surface_y = 8 * rowHeight + rowHeight / 2 - surface_rect.height / 2
        # Select rectangle 1P / 2P
        if(screenPos == 17 and tempPos != None):
            tempPos = tempPos - 9
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2 - columnWidth / 2
            surface_y = (tempPos + 6) * rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 18):
            surface_x = 5
            surface_y = 10 + surface_rect.height
        if(screenPos == 19):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = 10 + surface_rect.height
        if(screenPos == 20):
            surface_x = screen.get_width() - surface_rect.width - 5
            surface_y = 10 + surface_rect.height


        # Transparency
        if(alpha != None and color != None):
            surface.set_alpha(alpha)
            surface.fill(color)

        # Render surface
        screen.blit(surface, [surface_x, surface_y])







