import pygame
from pygame.locals import *

BUTTON_DOWN = 1
UP = (1, -1)
RIGHT = (0, 1)
DOWN = (1, 1)
LEFT = (0, -1)
STILL = (0, 0)
RED_BUTTON = 0
YELLOW_BUTTON = 1
BLACK_BUTTON = 2
BLUE_BUTTON = 3

class InputReader:

    def __init__(self):

        # Initialize joysticks
        pygame.joystick.init()
        self.joystick_count = pygame.joystick.get_count()
        if(self.joystick_count > 0):
            self.joysticks = [pygame.joystick.Joystick(i) for i in range(self.joystick_count)]
            for i in range(self.joystick_count):
                self.joysticks[i].init()
        self.actions = ['left', 'right', 'up', 'down', 'execute', 'undo', 'back']
        self.joystick_inputs = {LEFT : 'left', RIGHT : 'right', UP : 'up', DOWN : 'down', RED_BUTTON : 'execute', YELLOW_BUTTON : 'undo', BLACK_BUTTON : 'back', BLUE_BUTTON: None, STILL : 'center'}
        self.keyboard_inputs = ({K_LEFT : 'left', K_RIGHT : 'right', K_UP : 'up', K_DOWN : 'down', K_RETURN : 'execute', K_KP_ENTER : 'undo', K_ESCAPE : 'back'},
                                {K_a : 'left', K_d : 'right', K_w : 'up', K_s : 'down', 32 : 'execute', K_KP_ENTER : 'undo', K_ESCAPE : 'back'})

    def readInput(self, event):
        actions = {}
        if(event.type == pygame.KEYDOWN):
            actions = self.readKeyboardInput(event)
        elif(event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN):
            actions = self.readJoystickInput(event)
        if actions != {}: return list(actions.items())[0]
        else: return None

    def readJoystickInput(self, input):

        actions = {}
        if input.type == JOYAXISMOTION:
            joystick_input = (input.axis, int(round(self.joysticks[input.joy].get_axis(input.axis))))
            if joystick_input in self.joystick_inputs:
                actions[input.joy] = self.joystick_inputs[joystick_input]

        elif input.type == JOYBUTTONDOWN:
            if input.button in self.joystick_inputs:
                actions[input.joy] = self.joystick_inputs[input.button]

        return actions


    def readKeyboardInput(self, input):
        actions = {}
        for i in range(len(self.keyboard_inputs)):
            if input.key in self.keyboard_inputs[i]:
                actions[i] = self.keyboard_inputs[i][input.key]
        return actions