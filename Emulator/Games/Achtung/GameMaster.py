import pygame
from pygame.locals import *
import os, sys
from Games.Achtung.Snake import *
from random import randint
from math import *

class GameMaster:
    """ The main class of the game,
    handles initialization and running of the game """


    def __init__(self, width = 640, height = 480, screen = None):

        """ Initialize PyGame """
        self.path = str(os.path.dirname(os.path.realpath(__file__)))
        self.width = width
        self.height = height
        if screen == None:
            self.screen = pygame.display.set_mode([self.width, self.height])
            pygame.display.set_caption('SNEK 0.1')
        else:
            self.screen = screen
        self.background_color = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.tick = 10
        self.font = pygame.font.Font(None, 46)
        self.font2 = pygame.font.SysFont('monospace', 16)
        self.font3 = pygame.font.SysFont('monospace', 20)
        self.versionFont = pygame.font.SysFont('monospace', 16)
        self.arcadeFont = pygame.font.Font(self.path + "\ARCADE_I.ttf", 20)
        self.arcadeFontSmall = pygame.font.Font(self.path + "\ARCADE_I.ttf", 18)
        self.arcadeFontNormal = pygame.font.Font(self.path + "\ARCADE_N.ttf", 14)
        self.gameIsOver = False
        self.gamePaused = False
        self.score = 0
        self.score_tick = 0
        self.BLUE = (51, 51, 255)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 102)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 51, 51)
        self.PINK = (255, 0, 255)
        self.version = 0.1
        self.score_margin = 48
        self.score_file = self.path + '\hs.txt'
        self.currentHighScore = self.getHighScore()
        self.wall_rects = []
        self.snakes = 1
        self.snake = []
        self.pellet_width = 8
        self.pellet_height = 8
        self.snake_width = 16
        self.snake_height = 16
        self.colors = [self.RED, self.BLUE]
        self.winner = None
        self.winningScore = 150
        #pygame.mixer.init()
        self.slamSound = pygame.mixer.Sound(self.path + '\explosion.wav')
        self.coinSound = pygame.mixer.Sound(self.path + '\collision.wav')
        #self.highScoreSound = pygame.mixer.Sound('jingle_win.wav')
        self.gameOverSound = pygame.mixer.Sound(self.path + '\game_over2.wav')


    def checkPelletCollision(self, snake, pellets):
        pelletCols = pygame.sprite.spritecollide(snake, pellets, True)
        snake.pellets = snake.pellets + len(pelletCols)
        if (len(pelletCols) == 1):
            self.coinSound.play()
            pellets.add(Pellet(
                pygame.Rect(randint(1, self.width / snake.width - 2) * snake.width + snake.width / 4,
                            randint(10,
                                    self.height / snake.height - 2) * snake.height + snake.height / 4,
                            snake.pellet_width, snake.pellet_height)))
            snake.length = snake.length + 1
            snake.tailImage.append(pygame.Surface((snake.width, snake.height)))
            snake.tailRect.append(snake.tailImage[-1].get_rect())
            snake.score += 10
            self.score_tick += 1
            self.tick = 10 * exp(self.score_tick / 40)

    def updateNextMove(self, snake):
        if (snake.current_dir == 'left'):
            snake.next_move.x = snake.rect.x - snake.width
            snake.next_move.y = snake.rect.y
        elif (snake.current_dir == 'right'):
            snake.next_move.x = snake.rect.x + snake.width
            snake.next_move.y = snake.rect.y
        elif (snake.current_dir == 'up'):
            snake.next_move.x = snake.rect.x
            snake.next_move.y = snake.rect.y - snake.height
        elif (snake.current_dir == 'down'):
            snake.next_move.x = snake.rect.x
            snake.next_move.y = snake.rect.y + snake.height

    def checkWallCollision(self, snake, walls):
        snake.banned_move = None
        wallCols = snake.next_move.collidelist(walls)

        if (wallCols != -1):
            if (wallCols == 0):
                snake.banned_move = 'left'
            elif (wallCols == 2):
                snake.banned_move = 'right'
            elif (wallCols == 1):
                snake.banned_move = 'up'
            elif (wallCols == 3):
                snake.banned_move = 'down'

    def checkScore(self, snake, winningScore):
        return snake.score >= winningScore

    def mainLoop(self):
        """ Main loop of the game """
        if(self.snakes == 1):
            pygame.mixer.music.load(self.path + '\cosmic.mp3')
        else:
            pygame.mixer.music.load(self.path + '\\twoplayer.mp3')
        pygame.mixer.music.play(-1)

        self.loadSprites()
        while not self.gameIsOver:
            for snake in range(self.snakes):
                self.snake[snake].key_registered = False

            """ Loop events """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT)
                        or (event.key == K_LEFT)
                        or (event.key == K_UP)
                        or (event.key == K_DOWN)):
                        if not self.snake[0].key_registered and self.snake[0].stunned == 0:
                            self.snake[0].setDirection(event.key)
                            self.snake[0].key_registered = True
                    if ((event.key == K_d)
                          or (event.key == K_a)
                          or (event.key == K_w)
                          or (event.key == K_s)):
                        if not self.snake[1].key_registered and self.snake[1].stunned == 0:
                            self.snake[1].setDirection(event.key)
                            self.snake[1].key_registered = True
                    if (event.key == K_p):
                        if(self.gamePaused):
                            self.gamePaused = False
                        else:
                            self.gamePaused = True
                    elif (event.key == K_q):
                        sys.exit()
                    elif (event.key == K_ESCAPE):
                        return False

            if not self.gamePaused:
                for snake in range(self.snakes):

                    """ Pellet collision detection """
                    self.checkPelletCollision(self.snake[snake], self.pellet_sprites)

                    """ Wall collision detection """
                    self.updateNextMove(self.snake[snake])
                    self.checkWallCollision(self.snake[snake], self.wall_rects)

                    """ Tail collision detection """
                    if(self.snake[snake].checkTailCollision()):
                        self.winner = (-1 * snake) + 2
                        self.gameIsOver = True
                        pygame.mixer.music.stop()
                        return True

                    if(self.snakes == 2):

                        """ Check if there is a winner """
                        if (self.checkScore(self.snake[snake], self.winningScore)):
                            self.gameIsOver = True
                            pygame.mixer.music.stop()
                            return True

                        """ Snake collision detection """
                        if(self.snake[snake].checkSnakeCollision(self.snake[(-1 * snake) + 1])):
                            self.slamSound.play()
                            self.snake[snake].stunned = self.snake[snake].stun_time
                            self.snake[snake].stun_time += 5

                    """ Auto movement """
                    self.snake[snake].move()

            """ Render objects """
            self.drawObjects()
            pygame.display.flip()
            self.clock.tick(self.tick)


    def loadSprites(self):
        # Snake
        self.snake_sprites = pygame.sprite.Group()
        for i in range(self.snakes):
            self.snake.append(Snake((i+1) * 10 * 16, (i+1) * 10 * 16, self.colors[i]))
            self.snake_sprites.add(self.snake[i])
            #self.snake_sprites = pygame.sprite.RenderPlain((self.snake))

        # Pellet
        self.pellet_sprites = pygame.sprite.Group()
        self.pellet_sprites.add(Pellet(
                pygame.Rect(randint(1, self.width / self.snake_width - 2) * self.snake_width + self.snake_width / 4,
                            randint(10,
                                    self.height / self.snake_height - 2) * self.snake_height + self.snake_height / 4,
                            self.pellet_width, self.pellet_height)))

        self.score_margin_bg = pygame.Rect(0, 0, self.width, self.score_margin)

        # Walls
        wall_thickness = self.snake[0].width
        self.wall_rects.append(
            pygame.Rect(0, self.score_margin + wall_thickness, wall_thickness,
                        self.height - self.score_margin - 2 * wall_thickness))
        self.wall_rects.append(
            pygame.Rect(0, self.score_margin, self.width, wall_thickness))
        self.wall_rects.append(pygame.Rect(self.width - wall_thickness, self.score_margin + wall_thickness, wall_thickness,
                                           self.height - self.score_margin - 2 * wall_thickness))
        self.wall_rects.append(pygame.Rect(0, self.height - wall_thickness, self.width, wall_thickness))

    def drawObjects(self):
        """ Render objects """
        self.screen.fill(self.YELLOW)  # Background
        self.pellet_sprites.draw(self.screen)  # Pellet
        self.snake_sprites.draw(self.screen)  # Snake heads
        # if(self.snake[snake].tailRect):
        for snake in range(len(self.snake)):  # Snake tails
            for i in range(len(self.snake[snake].tailRect), -1, -1):
                pygame.draw.rect(self.screen, self.snake[snake].color, self.snake[snake].tailRect[i - 1])
        for j in range(len(self.wall_rects)):  # Walls
            pygame.draw.rect(self.screen, self.RED, self.wall_rects[j - 1])

        pygame.draw.rect(self.screen, self.YELLOW, self.score_margin_bg)
        # pygame.draw.rect(self.screen, (255, 0, 255), self.snake.next_move)

        for snake in range(self.snakes):
            # Score
            scoretext = self.arcadeFontNormal.render("Score: {0}".format(self.snake[snake].score), 1,
                                                     self.colors[snake])
            self.screen.blit(scoretext, (5 + snake * (self.width - scoretext.get_rect().width - 10), 10))

        if (self.snakes == 1):
            # Highscore
            highScoreText = self.arcadeFontNormal.render('Highscore: {0}'.format(self.currentHighScore[1]), 1,
                                                         self.BLUE)
            highScoreText2 = self.arcadeFontNormal.render('Set by: {0}'.format(self.currentHighScore[0]), 1,
                                                          self.BLUE)
            highScoreText_rect = highScoreText.get_rect()
            highScoreText2_rect = highScoreText2.get_rect()
            self.screen.blit(highScoreText, (self.width - highScoreText_rect.width - 10, 10))
            self.screen.blit(highScoreText2,
                             (self.width - highScoreText2_rect.width - 10, 10 + highScoreText_rect.height))

    def drawSurface(self, surface, screenPos, alpha = None, tempPos = None, color = None):
        """ Draws a surface at defined logical screen position """

        rowHeight = round(self.height/10)
        columnWidth = round(self.width/4)
        surface_x = 0
        surface_y = 0
        surface_rect = surface.get_rect()
        logoMargin = 20

        """ Check for screen positions """

        """ Version text """
        if(screenPos == 0):
            surface_x = self.screen.get_width() / 2 - surface_rect.width / 2
            surface_y = 1*rowHeight
        """ Game logo """
        if(screenPos == 1):
            surface_x = self.screen.get_width() / 2 - surface_rect.width / 2
            surface_y = 2*rowHeight
        """ Version text """
        if(screenPos == 2):
            surface_x = self.screen.get_width() / 2 - surface_rect.width / 2
            surface_y = self.screen.get_height() / 2 + surface_rect.height
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
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2
            surface_y = 6*rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 10):
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2
            surface_y = 7*rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Select rectangle """
        if(screenPos == 13 and tempPos != None):
            surface_x = self.screen.get_width() / 2 - surface_rect.width / 2
            surface_y = (2 + tempPos) * rowHeight + rowHeight / 2 - surface_rect.height / 2
        """ Alten logo (top right corner) """
        if(screenPos == 14):
            surface_x = self.screen.get_width() - logoMargin - surface_rect.width
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
        """ temppos 0 or 1 """
        if(screenPos == 17 and tempPos != None):
            tempPos = tempPos - 9
            surface_x = 3 * columnWidth + columnWidth / 2 - surface_rect.width / 2
            surface_y = (tempPos + 6) * rowHeight + rowHeight / 2 - surface_rect.height / 2
        if(screenPos == 18):
            surface_x = 5
            surface_y = 10 + surface_rect.height
        if(screenPos == 19):
            surface_x = self.width / 2 - surface_rect.width / 2
            surface_y = 10 + surface_rect.height
        if(screenPos == 20):
            surface_x = self.width - surface_rect.width - 5
            surface_y = 10 + surface_rect.height

            #self.screen.blit(winnerText,
            #                 (self.width - winnerText.get_rect().width - 10, 10 + winnerText.get_rect().height))

        """ Transparency """
        if(alpha != None and color != None):
            #surface.fill((255, 255, 255, alpha))
            surface.set_alpha(alpha)
            surface.fill(color)

        """ Render surface """
        self.screen.blit(surface, [surface_x, surface_y])


    def gameOver(self):
        """ Triggers game over screen with play again prompt """

        """ Define choosable screen positions """
        selectablePos = [15, 16]
        selectPosIndex = 0
        fontColor = self.RED
        pygame.mixer.music.load(self.path + '\game_over_loop.mp3')
        self.gameOverSound.play()
        pygame.mixer.music.queue(self.path + '\game_over_loop.mp3')
        pygame.mixer.music.play(-1)
        if(self.snakes == 1):
            self.highScore()
        else:
            if(self.winner == None):
                if(self.snake[0].score > self.snake[1].score):
                    self.winner = 1
                    fontColor = self.colors[0]
                else:
                    self.winner = 2
                    fontColor = self.colors[1]
            else:
                fontColor = self.colors[self.winner - 1]
            winnerText = self.arcadeFontNormal.render('Player ' + str(self.winner) + ' wins!', True, fontColor)

        """ Define objects to be rendered """
        retryText = self.arcadeFont.render('Play again?', True, fontColor)
        yesText = self.arcadeFont.render('Yes', True, fontColor)
        noText = self.arcadeFont.render('No', True, fontColor)
        gameOverImage = pygame.image.load(self.path + '\erik400.png')
        gameOverImage = pygame.transform.scale(gameOverImage, (round(256 * 1.5), round(226 * 1.5)))
        selectSquare = pygame.Surface((60, 30))

        while 1:

            """ Loop events """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if(event.key == K_RETURN):
                        if(selectPosIndex == 0):
                            pygame.mixer.music.stop()
                            return True
                        if(selectPosIndex == 1):
                            pygame.mixer.music.stop()
                            return False
                    elif(event.key == K_RIGHT):
                        if(selectPosIndex + 1 < len(selectablePos)):
                            selectPosIndex += 1
                    elif(event.key == K_LEFT):
                        if(selectPosIndex - 1 >= 0):
                            selectPosIndex -= 1
                    elif(event.key == K_q):
                        sys.exit()

            """ Render objects """
            self.drawObjects()
            self.drawSurface(retryText, 5)
            self.drawSurface(yesText, 15)
            self.drawSurface(noText, 16)
            self.drawSurface(gameOverImage, 0)
            if (self.snakes == 2):
                self.drawSurface(winnerText, 18 + (self.winner - 1) * 2)
                #self.screen.blit(winnerText,
                #                 (self.width - winnerText.get_rect().width - 10, 10 + winnerText.get_rect().height))
            self.drawSurface(selectSquare, 15, 128, selectablePos[selectPosIndex], fontColor)
            pygame.display.flip()


    def startScreen(self):
        """ Player chooses mode and controllers """

        """ Define choosable screen positions """
        selectPosIndex = 0
        selectablePos = [4, 5, 6]
        selectPosIndexStartGame = 0
        selectablePosStartGame = [9, 10]
        startGame = False
        pygame.mixer.music.load(self.path + '\\right_back_into_you.mp3')
        pygame.mixer.music.play(-1)

        while 1:

            """ Loop events """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if(event.key == K_q):
                        return False
                    if(event.key == K_RETURN):
                        if(startGame):
                            if(selectPosIndexStartGame == 0):
                                pygame.mixer.music.stop()
                                return True
                            if(selectPosIndexStartGame == 1):
                                self.snakes = 2
                                pygame.mixer.music.stop()
                                return True
                        else:
                            if(selectPosIndex == 0):
                                startGame = True
                            if(selectPosIndex == 1):
                                self.showTop10()
                            if(selectPosIndex == 2):
                                pygame.mixer.music.stop()
                                return False
                    if(event.key == K_DOWN):
                        if(startGame):
                            if(selectPosIndexStartGame + 1 < len(selectablePosStartGame)):
                                selectPosIndexStartGame += 1
                        else:
                            if(selectPosIndex + 1 < len(selectablePos)):
                                selectPosIndex += 1
                    if(event.key == K_UP):
                        if(startGame):
                            if (selectPosIndexStartGame - 1 >= 0):
                                selectPosIndexStartGame -= 1
                        else:
                            if(selectPosIndex - 1 >= 0):
                                selectPosIndex -= 1
                    if(event.key == K_ESCAPE):
                        pygame.mixer.music.stop()
                        return False

            menuTextColor = self.BLUE

            """ Define objects to be rendered """
            selectSquare = pygame.Surface((220, 30))
            selectSquareStartGame = pygame.Surface((50, 30))
            logoImage = pygame.image.load(self.path + '\SNEK_logo1.png')
            logoImage = pygame.transform.scale(logoImage, (400, 240))
            startGameText = self.arcadeFont.render('Start game', True, menuTextColor)
            optionsText = self.arcadeFont.render('High score', True, menuTextColor)
            quitText = self.arcadeFont.render('Quit', True, menuTextColor)
            versionText = self.versionFont.render('Version ' + str(self.version), True, self.RED)
            onePlayerText = self.arcadeFont.render('1P', True, menuTextColor)
            twoPlayerText = self.arcadeFont.render('2P', True, menuTextColor)
            #altenLogoImage = pygame.image.load('alten_logo.png')
            #altenLogoImage = pygame.transform.scale(altenLogoImage, (round(40*1.2), round(60*1.2)))

            """ Render objects """
            self.screen.fill(self.YELLOW)
            self.drawSurface(versionText, 2)
            self.drawSurface(startGameText, 4)
            self.drawSurface(optionsText, 5)
            self.drawSurface(quitText, 6)
            self.drawSurface(logoImage, 1)
            if(startGame):
                self.drawSurface(onePlayerText, 9)
                self.drawSurface(twoPlayerText, 10)
                self.drawSurface(selectSquareStartGame, 17, 128, selectablePosStartGame[selectPosIndexStartGame], menuTextColor)
            else:
                self.drawSurface(selectSquare, 13, 128, selectablePos[selectPosIndex], menuTextColor)

            pygame.display.flip()

    def getHighScore(self):
        score_file = open(self.score_file, 'r')
        lines = score_file.readlines()
        score_file.close()

        high_score = 0
        high_name = ' '

        for line in lines:
            name, score = line.strip().split(' ')
            score = int(score)

            if(score > high_score):
                high_score = score
                high_name = name

        return high_name, high_score

    def writeScore(self, name):
        score_file = open(self.score_file, 'a')
        print(name, self.snake[0].score, file = score_file)
        score_file.close()

    def showTop10(self):
        windowWidth = round(self.width * 0.7)#450
        windowHeight = round(self.height * 0.85)#400
        entry_spacing = 30
        fontColor = self.WHITE
        backgroundColor = self.BLUE
        all_score = []

        """ Get top 10 """
        score_file = open(self.score_file, 'r')
        lines = score_file.readlines()
        for line in lines:
            sep = line.index(' ')
            name = line[:sep]
            score = int(line[sep+1:-1])
            all_score.append((score, name))
        score_file.close()
        all_score.sort(reverse = True)
        top10 = all_score[:10]

        """ Create high score window and render text"""
        box = pygame.Surface((windowWidth, windowHeight))
        box.fill(backgroundColor)
        pygame.draw.rect(box, self.BLACK, (0, 0, windowWidth, windowHeight), 1)
        txt_surf = self.arcadeFont.render("HIGHSCORE", True, fontColor)
        txt_rect = txt_surf.get_rect(center = (windowWidth // 2, round(0.075 * windowHeight)))
        box.blit(txt_surf, txt_rect)
        txt_surf = self.arcadeFontSmall.render("Press ENTER to continue", True, fontColor)
        txt_rect = txt_surf.get_rect(center = (windowWidth // 2, windowHeight - round(0.075 * windowHeight)))
        box.blit(txt_surf, txt_rect)

        """ Render top 10 """
        for i, entry in enumerate(top10):
            txt_surf = self.arcadeFontNormal.render(entry[1] + "  " + str(entry[0]), True, fontColor)
            txt_rect = txt_surf.get_rect(center = (windowWidth // 2, entry_spacing * i + round(windowHeight / 6)))
            box.blit(txt_surf, txt_rect)

        """ Render the high score window """
        self.screen.blit(box, (self.width / 2 - windowWidth / 2, self.height / 2 - windowHeight / 2))
        pygame.display.flip()

        """ Wait for user input to continue """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    return
            pygame.time.wait(20)

    def getLastTop10(self):
        all_score = []

        score_file = open(self.score_file, 'r')
        lines = score_file.readlines()
        for line in lines:
            sep = line.index(' ')
            name = line[:sep]
            score = int(line[sep + 1:-1])
            all_score.append((score, name))
        score_file.close()
        all_score.sort(reverse = True)
        lastPerson = all_score[9]
        lastScore = lastPerson[0]
        return lastScore


    def highScore(self):

        high_name, high_score = self.getHighScore()

        if(self.snake[0].score > high_score):
            #self.highScoreSound.play()
            name = self.promptBox('WOW!!', 'You have beaten the highscore!')
            self.writeScore(name)
        elif(self.snake[0].score == high_score):
            #self.highScoreSound.play()
            name = self.promptBox('Great job!', 'You equalised the highscore!')
            self.writeScore(name)
        elif(self.snake[0].score > self.getLastTop10()):
            #self.highScoreSound.play()
            name = self.promptBox('Well played!', 'You have made it into the top 10!')
            self.writeScore(name)

    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
        rect = Rect(rect)
        y = rect.top
        lineSpacing = 5

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def promptBox(self, txt, txt2):

        windowWidth = self.width / 2
        windowHeight = self.height / 2
        backgroundColor = self.BLUE
        fontColor = self.WHITE
        nameFont = self.arcadeFont

        """ Function for showing the typed name """
        def show_name(screen, box, name, color, font):
            #pygame.draw. rect(box, color, (50, 60, windowWidth-100, 20), 0)
            txt_surf = font.render(name, True, color)
            txt_rect = txt_surf.get_rect(center = (windowWidth / 2, round(windowHeight - windowHeight * 0.2)))
            box.blit(txt_surf, txt_rect)
            screen.blit(box, (windowWidth // 2, windowHeight // 2))
            pygame.display.flip()

        box = pygame.Surface((windowWidth, windowHeight))
        txt_surf = self.arcadeFont.render(txt, True, fontColor)
        txt_rect = txt_surf.get_rect(center = (windowWidth / 2, round(0.1 * windowHeight)))
        txt2_surf = self.arcadeFontNormal.render(txt2, True, fontColor)
        #txt2_rect = txt2_surf.get_rect(center = (windowWidth / 2, round(0.2 * windowHeight)))
        txt2_rect = pygame.Rect(round(windowWidth * 0.15), round(windowHeight * 0.3), round(windowWidth * 0.8), 50)

        txt3_surf = self.arcadeFontNormal.render('What is your name?', True, fontColor)
        txt3_rect = txt3_surf.get_rect(center = (windowWidth / 2, round(0.6 * windowHeight)))

        name = ''

        while True:
            box.fill(backgroundColor) # Background
            pygame.draw.rect(box, self.BLACK, (0, 0, windowWidth, windowHeight), 1)  # Black edge
            box.blit(txt_surf, txt_rect) # Congratulation text
            self.drawText(box, txt2, fontColor, txt2_rect, self.arcadeFontNormal)
            #box.blit(txt2_surf, txt2_rect)
            box.blit(txt3_surf, txt3_rect)

            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif(event.type == pygame.KEYDOWN):
                    inkey = event.key
                    if(inkey in [13, 271]):
                        return name
                    elif(inkey == 8):
                        name = name[:-1]
                    elif(inkey <= 300):
                        if(pygame.key.get_mods() & pygame.KMOD_SHIFT and 122 >= inkey >= 97):
                            inkey -= 32
                        name += chr(inkey)
            show_name(self.screen, box, name, fontColor, nameFont)
            pygame.display.flip()
