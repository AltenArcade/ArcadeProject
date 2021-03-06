from os import path
from platform import system
from Games.SNEK.Classes import *
from random import randint
from math import exp
from InputReader import *

class GameMaster:

    """ The main class of the game,
    handles initialization and running of the game """


    def __init__(self, width = 1280, height = 800, screen = None):

        extension = '\\'
        if system() == "Linux":
            extension = '/'
        self.path = str(path.dirname(path.realpath(__file__))) + extension
        self.sound_path = self.path + 'sound' + extension
        self.img_path = self.path + 'img' + extension
        self.font_path = self.path + 'fonts' + extension
        if screen == None:
            self.width = width
            self.height = height
            self.screen = pygame.display.set_mode([self.width, self.height])
        else:
            self.screen = screen
            self.width = screen.get_width()
            self.height = screen.get_height()
        self.clock = pygame.time.Clock()
        self.tick = 10
        self.gameIsOver = False
        self.gamePaused = False
        self.score_tick = 0
        self.version = 0.1
        self.score_margin = 48
        self.score_file = self.path + 'hs.txt'
        self.currentHighScore = self.getHighScore()
        self.walls = []
        self.snakes = 1
        self.snake = []
        self.nx = 40
        self.ny = 25
        self.snake_size = self.width / self.nx
        self.pellet_size = self.snake_size / 2
        self.score_margin =  2 * self.snake_size
        self.colors = [RED, BLUE]
        self.winner = None
        self.score_win = False
        self.winningScore = 150
        self.DJ = DJ(self.sound_path)
        self.Painter = Painter([self.screen.get_width(), self.screen.get_height()], self.score_margin, self.img_path, self.font_path)
        self.drawNextMove = False
        self.InputReader = InputReader()
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'x', 'y', 'z']
        self.winning_scores = [50, 100, 150, 200]

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

    def checkScore(self, snake, winningScore):
        return snake.score >= winningScore

    def addPellet(self):
        self.pellet_sprites.add(Pellet(randint(1, self.width / self.snake_size - 2) * self.snake_size + self.snake_size / 2 - self.pellet_size / 2,
                                       randint(10, self.height / self.snake_size - 2) * self.snake_size + self.snake_size / 2 - self.pellet_size / 2,
                                       self.pellet_size, self.Painter.pellet_color))

    def increaseUpdateFreq(self):
        self.score_tick += 1
        self.tick = 10 * exp(self.score_tick / 40)

    def mapAction(self, snake_and_action):

        action = snake_and_action[1]
        snake_nr = int(snake_and_action[0])
        if not (snake_nr + 1) > self.snakes:
            snake = self.snake[snake_nr]
            if action in ['left', 'right', 'up', 'down'] and not snake.key_registered:
                snake.setDirection(action)
                snake.key_registered = True
                return True
        if action == 'back':
            return False
        else:
            return True

    def mainLoop(self):
        '''
        Main loop of the game.
        :return: True/False if game is over.
        '''

        self.loadSprites()
        self.DJ.playGameMusic(self.snakes)
        self.score_win = False

        while not self.gameIsOver:
            for snake in range(self.snakes):
                self.snake[snake].key_registered = False

            # Loop events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Translate input to action
                action = self.InputReader.readInput(event)
                if action != None:
                    if self.mapAction(action) == False:
                        return False

            # Manage actions
            if not self.gamePaused:

                # Check each snake
                for snake in range(self.snakes):

                    # Pellet collision detection
                    if(self.snake[snake].checkPelletCollision(self.pellet_sprites)):
                        self.DJ.playPickUpSound()
                        self.snake[snake].increasePelletCount()
                        self.addPellet()
                        self.snake[snake].grow()
                        self.increaseUpdateFreq()

                    # Wall collision detection
                    self.snake[snake].checkWallCollision(self.walls)

                    # Tail collision detection
                    if(self.snake[snake].checkTailCollision()):
                        if(self.snakes == 2):
                            self.winner = (-1 * snake) + 2
                        self.gameIsOver = True
                        self.DJ.stopMusic()
                        return True

                    if(self.snakes == 2):

                        # Check if there is a winner
                        if (self.checkScore(self.snake[snake], self.winningScore)):
                            self.winner = snake + 1
                            self.gameIsOver = True
                            self.score_win = True
                            self.DJ.stopMusic()
                            return True

                        # Snake collision detection
                        if(self.snake[snake].checkSnakeCollision(self.snake[(-1 * snake) + 1]) and self.snake[snake].stunned == 0):
                            self.DJ.playCollisionSound()
                            self.snake[snake].stunned = self.snake[snake].stun_time
                            self.snake[snake].stun_time += 5

                    # Auto movement
                    self.snake[snake].move()
                    self.snake[snake].updateNextMove()

            # Render objects
            self.Painter.drawGameObjects(self.screen, [self.snake_sprites, self.pellet_sprites, self.wall_sprites], self.snake, self.score_window, self.currentHighScore, self.winningScore, self.snake_size)
            if(self.Painter.draw_next_move):
                self.Painter.drawNextMove(self.screen, self.snake[0])
                if(self.snakes == 2):
                    self.Painter.drawNextMove(self.screen, self.snake[1])
            pygame.display.flip()
            self.clock.tick(self.tick)


    def loadSprites(self):

        # Snake
        directions = ['right', 'left']
        start_positions = [(10, 10), (self.nx - 10, self.ny - 10)]
        self.snake_sprites = pygame.sprite.Group()
        for i in range(self.snakes):
            self.snake.append(
                Snake(start_positions[i][0] * self.snake_size,
                      start_positions[i][1] * self.snake_size,
                      self.colors[i],
                      self.snake_size,
                      directions[i]))
            self.snake_sprites.add(self.snake[i])

        # Pellet
        self.pellet_sprites = pygame.sprite.Group()
        self.addPellet()

        # Walls
        wall_thickness = self.snake_size

        self.walls.append(Wall(0,
                               self.score_margin + wall_thickness,
                               wall_thickness,
                               self.height - self.score_margin - 2 * wall_thickness,
                               self.Painter.wall_color))
        self.walls.append(Wall(0,
                               self.score_margin,
                               self.width,
                               wall_thickness,
                               self.Painter.wall_color))
        self.walls.append(Wall(self.width - wall_thickness,
                               self.score_margin + wall_thickness,
                               wall_thickness,
                               self.height - self.score_margin - 2 * wall_thickness,
                               self.Painter.wall_color))
        self.walls.append(Wall(0,
                               self.height - wall_thickness,
                               self.width,
                               wall_thickness,
                               self.Painter.wall_color))

        self.wall_sprites = pygame.sprite.Group()
        for wall in range(len(self.walls)):
            self.wall_sprites.add(self.walls[wall])


        # Score window
        self.score_window = pygame.Surface((self.width, self.score_margin))

    def gameOver(self):
        '''
        Game over screen with play again prompt
        :return: None
        '''

        # Define selectable screen positions
        selectablePos = [15, 16]
        selectPosIndex = 0
        fontColor = RED

        # Play game over music
        self.DJ.playGameOverMusic()

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


        while True:

            # Loop events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                action = self.InputReader.readInput(event)
                if action != None:
                    action = action[1]
                    if action == 'execute':
                        if (selectPosIndex == 0):
                            self.DJ.stopMusic()
                            return [True, self.winningScore]
                        if (selectPosIndex == 1):
                            self.DJ.stopMusic()
                            return [False, None]
                    if action == 'right':
                        if (selectPosIndex + 1 < len(selectablePos)):
                            selectPosIndex += 1
                    if action == 'left':
                        if (selectPosIndex - 1 >= 0):
                            selectPosIndex -= 1
                    if action == 'back':
                        self.DJ.stopMusic()
                        return [False, None]

            # Draw game objects
            self.Painter.drawGameObjects(self.screen, [self.snake_sprites, self.pellet_sprites, self.wall_sprites],
                                         self.snake, self.score_window, self.currentHighScore, self.winningScore, self.snake_size)

            # Draw game over screen
            self.Painter.drawGameOverScreen(self.screen, selectablePos, selectPosIndex, fontColor, self.score_win, self.winner)


    def startScreen(self):

        '''
        Welcome screen where the user chooses mode and can check highscore.
        :return: True/False if game is ready to start.
        '''

        # Define choosable screen positions
        selectPosIndex = 0
        selectablePos = [4, 5, 6]
        selectPosIndexStartGame = 0
        selectablePosStartGame = [9, 10]
        startGame = False

        # Play intro music
        self.DJ.playIntroMusic()

        while 1:

            # Loop events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                action = self.InputReader.readInput(event)
                if action != None:
                    action = action[1]
                    if action == 'execute':
                        if (startGame):
                            if (selectPosIndexStartGame == 0):
                                self.DJ.stopMusic()
                                return True
                            if (selectPosIndexStartGame == 1):
                                self.snakes = 2
                                self.winningScore = self.promptBox(self.winning_scores, 'number', ['Let the largest snake win!', 'Rules: First to reach score limit wins.', 'Please choose score limit:'], LIGHT_YELLOW, BLACK, RED)
                                self.DJ.stopMusic()
                                return True
                        else:
                            if (selectPosIndex == 0):
                                startGame = True
                            if (selectPosIndex == 1):
                                self.showTop10()
                            if (selectPosIndex == 2):
                                self.DJ.stopMusic()
                                return False
                    if action == 'down':
                        if (startGame):
                            if (selectPosIndexStartGame + 1 < len(selectablePosStartGame)):
                                selectPosIndexStartGame += 1
                        else:
                            if (selectPosIndex + 1 < len(selectablePos)):
                                selectPosIndex += 1
                    if action == 'up':
                        if (startGame):
                            if (selectPosIndexStartGame - 1 >= 0):
                                selectPosIndexStartGame -= 1
                        else:
                            if (selectPosIndex - 1 >= 0):
                                selectPosIndex -= 1
                    if action == 'back':
                        self.DJ.stopMusic()
                        return False

            # Draw start screen
            self.Painter.drawStartScreen(self.screen, startGame, selectablePos, selectPosIndex, selectablePosStartGame, selectPosIndexStartGame)


    def getHighScore(self):


        if path.isfile(self.score_file):
            score_file = open(self.score_file, 'r')
        else:
            score_file = open(self.score_file, 'w+')
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
        windowWidth = round(self.width * 0.5)
        windowHeight = round(self.height * 0.85)
        all_score = []

        # Get top 10
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

        self.Painter.drawHighscoreWindow(self.screen, [windowWidth, windowHeight], top10)

        # Wait for user input to continue
        while True:
            for event in pygame.event.get():
                action = self.InputReader.readInput(event)
                if action != None:
                    action = action[1]
                    if action == 'execute':
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
        if len(all_score) >= 10:
            lastPerson = all_score[9]
        else:
            lastPerson = all_score[-1]
        lastScore = lastPerson[0]
        return lastScore


    def highScore(self):

        high_name, high_score = self.getHighScore()

        if(self.snake[0].score > high_score):
            name = self.promptBox(self.alphabet, 'name', ['WOW!!', 'You have beaten the highscore!', 'Enter your name:'], BLUE, WHITE, BLACK)
            self.writeScore(name)
        elif(self.snake[0].score == high_score):
            name = self.promptBox(self.alphabet, 'name', ['Great job!', 'You equalised the highscore!', 'Enter your name:'], BLUE, WHITE, BLACK)
            self.writeScore(name)
        elif(self.snake[0].score > self.getLastTop10()):
            name = self.promptBox(self.alphabet, 'name', ['Well played!', 'You have made it into the top 10!', 'Enter your name:'], BLUE, WHITE, BLACK)
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

            surface.blit(image, (rect.centerx / 2, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def promptBox(self, data, entry_type, strings, background_color, font_color, border_color, headline_color = None):

        windowWidth = self.width / 2
        windowHeight = self.height / 2
        nameFont = self.Painter.arcadeFont
        index = 0
        current_element = data[index]
        done = False

        # Function for showing the typed name
        def show_name(screen, box, name, color, font):
            txt_surf = font.render(name, True, color)
            txt_rect = txt_surf.get_rect(center = (windowWidth / 2, round(windowHeight - windowHeight * 0.2)))
            box.blit(txt_surf, txt_rect)
            screen.blit(box, (windowWidth / 2, windowHeight / 2))

        box = pygame.Surface((windowWidth, windowHeight))
        sub_box1 = pygame.Surface((windowWidth, round(windowHeight * 0.8)))

        name = ''
        while not done:
            box.fill(background_color) # Background

            for event in pygame.event.get():
                action = self.InputReader.readInput(event)
                if action != None:
                    action = action[1]
                    if action == 'back':
                        done = True
                    elif action == 'down':
                        if (index == len(data) - 1):
                            index = 0
                        else:
                            index += 1
                        current_element = data[index]
                    elif action == 'up':
                        if (index == 0):
                            index = len(data) - 1
                        else:
                            index -= 1
                        current_element = data[index]
                    if entry_type == 'name':
                        if action == 'right':
                            name = name + current_element
                        elif action == 'left':
                            name = name[:-1]
                        elif action == 'execute':
                            return name + current_element
                    elif entry_type == 'number':
                        if action == 'execute':
                            return current_element

            # Draw info text
            for idx, string in enumerate(strings):
                sub_surface = pygame.Surface((sub_box1.get_width(), round(sub_box1.get_height() / len(strings))))
                sub_surface.fill(background_color)
                if idx == 0 and headline_color != None:
                    fontColor = headline_color
                else:
                    fontColor = font_color
                if idx == 1:
                    txt_surf = self.Painter.arcadeFontMedium.render(string, True, fontColor)
                else:
                    txt_surf = self.Painter.arcadeFont.render(string, True, fontColor)
                sub_surface.blit(txt_surf, txt_surf.get_rect(center = (sub_surface.get_width() / 2, sub_surface.get_height() / 2)))
                sub_box1.blit(sub_surface, (0, (idx / len(strings)) * sub_box1.get_height()))
                box.blit(sub_box1, (0, 0))
            pygame.draw.rect(box, border_color, (0, 0, windowWidth, windowHeight), 1)
            if entry_type == 'name':
                show_name(self.screen, box, name + current_element, fontColor, nameFont)
            elif entry_type == 'number':
                show_name(self.screen, box, str(current_element), fontColor, nameFont)
            pygame.display.flip()
