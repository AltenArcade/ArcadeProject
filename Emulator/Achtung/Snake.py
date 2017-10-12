import pygame
from pygame.locals import *

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

    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = 16
        self.height = 16
        self.color = color#(255, 51, 51)
        self.pellet_width = 8
        self.pellet_height = 8

        """ Head """
        self.image = pygame.Surface((self.width, self.height))#pygame.image.load('snake.png')
        self.rect = self.image.get_rect()
        #self.rect.x = 10 * self.width
        self.rect.x = x
        #self.rect.y = 10 * self.height
        self.rect.y = y
        self.image.fill(self.color)

        """ Tail """
        self.tailImage = []
        self.tailRect = []

        self.length = 3
        self.pellets = 0
        self.score = 0
        self.score_tick = 0
        self.x_dist = self.width
        self.y_dist = self.height
        self.current_dir = 'right'
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
            """ Update movement of tail """
            for i in range(len(self.tailRect)-1, -1, -1):
                if(i == 0):
                    self.tailRect[i].x = self.rect.x
                    self.tailRect[i].y = self.rect.y
                else:
                    self.tailRect[i].x = self.tailRect[i-1].x
                    self.tailRect[i].y = self.tailRect[i-1].y

            """ Update movement of head """
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


    def setDirection(self, key):

        if (key != None):
            if ((key == K_RIGHT or key == K_d) and self.banned_move != 'right' and self.current_dir != 'left'):
                self.current_dir = 'right'
                self.next_move.x = self.rect.x + self.width
                self.next_move.y = self.rect.y
            elif ((key == K_LEFT or key == K_a) and self.banned_move != 'left' and self.current_dir != 'right'):
                self.current_dir = 'left'
                self.next_move.x = self.rect.x - self.width
                self.next_move.y = self.rect.y
            elif ((key == K_UP or key == K_w) and self.banned_move != 'up' and self.current_dir != 'down'):
                self.current_dir = 'up'
                self.next_move.x = self.rect.x
                self.next_move.y = self.rect.y - self.height
            elif ((key == K_DOWN or key == K_s) and self.banned_move != 'down' and self.current_dir != 'up'):
                self.current_dir = 'down'
                self.next_move.x = self.rect.x
                self.next_move.y = self.rect.y + self.height

    def checkTailCollision(self):
        return self.rect.collidelist(self.tailRect) != -1

    def checkSnakeCollision(self, snake):
        return self.rect.collidelist(snake.tailRect) != -1


class Pellet(pygame.sprite.Sprite):
    '''
    Pellet that the snake(s) can pick up.
    '''

    def __init__(self, rect = None):
        pygame.sprite.Sprite.__init__(self)
        self.width = 8
        self.height = 8
        self.color = (51, 51, 255)
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image.fill(self.color)
        if rect != None:
            self.rect = rect


class Wall(pygame.sprite.Sprite):
    '''
    Walls defining the game area.
    '''

    def __init__(self, image = None, rect = None, loc = None):
        pygame.sprite.Sprite.__init__(self)
        self.thickness = 20
        self.color = (255, 51, 51)
        #self.image = pygame.Surface((self.width, self.height))
        #self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect
        if loc != None:
            self.loc = loc
        if image != None:
            self.image = image
            self.image.fill(self.color)

class DJ():
    '''
    Class for playing music and sound effects.
    '''

    def __init__(self):

        # Define music songs
        self.introMusic = 'Achtung\\right_back_into_you.mp3'
        self.gameOverMusic = 'Achtung\game_over_loop.mp3'
        self.onePlayerMusic = 'Achtung\cosmic.mp3'
        self.twoPlayerMusic = 'Achtung\\twoplayer.mp3'

        # Define sound effects
        self.gameOverSound = pygame.mixer.Sound('Achtung\game_over2.wav')
        self.collisionSound = pygame.mixer.Sound('Achtung\explosion.wav')
        self.pickUpSound = pygame.mixer.Sound('Achtung\collision.wav')

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

    def __init__(self):
        self.font = pygame.font.Font(None, 46)
        self.font2 = pygame.font.SysFont('monospace', 16)
        self.font3 = pygame.font.SysFont('monospace', 20)
        self.versionFont = pygame.font.SysFont('monospace', 16)
        self.arcadeFont = pygame.font.Font('Achtung\ARCADE_I.ttf', 20)
        self.arcadeFontSmall = pygame.font.Font('Achtung\ARCADE_I.ttf', 18)
        self.arcadeFontNormal = pygame.font.Font('Achtung\ARCADE_N.ttf', 14)

        # Start screen
        self.startMenuTextColor = BLUE
        self.selectSquare = pygame.Surface((220, 30))
        self.selectSquareStartGame = pygame.Surface((50, 30))
        logoImage = pygame.image.load('Achtung\SNEK_logo1.png')
        self.logoImage = pygame.transform.scale(logoImage, (400, 240))
        self.startGameText = self.arcadeFont.render('Start game', True, self.startMenuTextColor)
        self.optionsText = self.arcadeFont.render('High score', True, self.startMenuTextColor)
        self.quitText = self.arcadeFont.render('Quit', True, self.startMenuTextColor)
        self.versionText = self.versionFont.render('Version ' + str(0.1), True, RED)
        self.onePlayerText = self.arcadeFont.render('1P', True, self.startMenuTextColor)
        self.twoPlayerText = self.arcadeFont.render('2P', True, self.startMenuTextColor)

    def drawStartScreen(self, screen, start_game, selectable_positions, selectable_position_index, selectable_positions_start_game, selectable_position_index_start_game):
        '''
        Draws the start screen of the game.
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

    #def drawGameObjects(self, screen, snakes, pellets, ):

    def drawSurface(self, screen, surface, screenPos, alpha = None, tempPos = None, color = None):

        """ Draws a surface at defined logical screen position """

        columnWidth = round(screen.get_size()[0] / 4)
        rowHeight = round(screen.get_size()[1] / 10)
        surface_x = 0
        surface_y = 0
        surface_rect = surface.get_rect()
        logoMargin = 20

        """ Check for screen positions """

        """ Version text """
        if(screenPos == 0):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = 1*rowHeight
        """ Game logo """
        if(screenPos == 1):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = 2*rowHeight
        """ Version text """
        if(screenPos == 2):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = screen.get_height() / 2 + surface_rect.height
        """ Menu position 2 """
        if(screenPos == 4):
            surface_x = 2*columnWidth - surface_rect.width / 2
            surface_y = 6*rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Menu position 3 """
        if(screenPos == 5):
            surface_x = 2*columnWidth - surface_rect.width / 2
            surface_y = 7*rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Menu position 4 """
        if(screenPos == 6):
            surface_x = 2*columnWidth - surface_rect.width / 2
            surface_y = 8*rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Menu position 5 """
        if(screenPos == 7):
            surface_x = 2 * columnWidth - surface_rect.width / 2
            surface_y = 9 * rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 9):
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2 - columnWidth / 2
            surface_y = 6*rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 10):
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2 - columnWidth / 2
            surface_y = 7*rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Select rectangle """
        if(screenPos == 13 and tempPos != None):
            surface_x = screen.get_width() / 2 - surface_rect.width / 2
            surface_y = (2 + tempPos) * rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Alten logo (top right corner) """
        if(screenPos == 14):
            surface_x = screen.get_width() - logoMargin - surface_rect.width
            surface_y = logoMargin
        """ Menu position 5a """
        if(screenPos == 15):
            if(tempPos != None):
                tempPos = tempPos - 14
                surface_x = tempPos * columnWidth + columnWidth / 2 - surface_rect.width / 2
                surface_y = 8 * rowHeight + rowHeight / 2 - surface_rect.height / 2
            else:
                surface_x = columnWidth + columnWidth / 2 - surface_rect.width / 2
                surface_y = 8 * rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Menu position 5b """
        if(screenPos == 16):
            surface_x = 2 * columnWidth + columnWidth / 2 - surface_rect.width / 2
            surface_y = 8 * rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Select rectangle 1P / 2P """
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


        """ Transparency """
        if(alpha != None and color != None):
            surface.set_alpha(alpha)
            surface.fill(color)

        """ Render surface """
        screen.blit(surface, [surface_x, surface_y])







