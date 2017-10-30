import pygame
from pygame.locals import *
from Games.SNEK.GameMaster import GameMaster

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

def AchtungMain(screen = None):
    running = True
    play = True
    firstPlay = True
    twoPlayers = False
    winningScore = None

    while running:
        if (screen != None):
            MainWindow = GameMaster(screen.get_size()[0],screen.get_size()[1], screen)
        else:
            MainWindow = GameMaster()
        if(firstPlay):
            play = MainWindow.startScreen()
            if(play):
                gameOver = MainWindow.mainLoop()
                if(gameOver):
                    retry = MainWindow.gameOver()
                    if (retry[0]):
                        firstPlay = False
                        if(MainWindow.snakes == 2):
                            twoPlayers = True
                            winningScore = MainWindow.winningScore
                        else:
                            twoPlayers = False
                    else:
                        firstPlay = True
                else:
                    running = True
            else:
                running = False
        else:
            if(twoPlayers):
                MainWindow.snakes = 2
                MainWindow.winningScore = winningScore
                #MainWindow.winningScore = retry[1]
            gameOver = MainWindow.mainLoop()
            if (gameOver):
                retry = MainWindow.gameOver()
                if (retry[0]):
                    firstPlay = False
                else:
                    firstPlay = True
            else:
                running = True
                firstPlay = True

if __name__ == '__main__':
    AchtungMain()

if __name__ == 'SNEK':
    AchtungMain()
