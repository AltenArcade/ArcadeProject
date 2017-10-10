import os, sys
import pygame
from pygame.locals import *
from Achtung.GameMaster import GameMaster

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

def AchtungMain(screen = None):
    running = True
    play = True
    firstPlay = True
    twoPlayers = False

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
                    if (retry):
                        firstPlay = False
                        if(MainWindow.snakes == 2):
                            twoPlayers = True
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
            gameOver = MainWindow.mainLoop()
            if (gameOver):
                retry = MainWindow.gameOver()
                if (retry):
                    firstPlay = False
                else:
                    firstPlay = True
            else:
                running = True
                firstPlay = True

if __name__ == '__main__':
    AchtungMain()
    """
    running = True
    play = True
    firstPlay = True
    twoPlayers = False

    while running:
        MainWindow = GameMaster()
        if(firstPlay):
            play = MainWindow.startScreen()
            if(play):
                gameOver = MainWindow.mainLoop()
                if(gameOver):
                    retry = MainWindow.gameOver()
                    if (retry):
                        firstPlay = False
                        if(MainWindow.snakes == 2):
                            twoPlayers = True
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
            gameOver = MainWindow.mainLoop()
            if (gameOver):
                retry = MainWindow.gameOver()
                if (retry):
                    firstPlay = False
                else:
                    firstPlay = True
            else:
                running = True
                firstPlay = True
    """


if __name__ == 'Achtung':
    AchtungMain()
