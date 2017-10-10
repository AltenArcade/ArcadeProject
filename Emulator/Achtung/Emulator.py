import Achtung
import pygame

if __name__ == '__main__':
    pygame.init()
    width = 640
    height = 480
    screen = pygame.display.set_mode([width, height])
    Achtung.main(screen)