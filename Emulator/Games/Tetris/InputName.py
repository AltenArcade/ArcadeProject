import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class InputName():

    def __init__(self, screen, score, font):
        pygame.init()
        self.name = ""
        self.screen = screen
        self.score = score
        self.board_width = self.screen.get_size()[0]
        self.board_height = self.screen.get_size()[1]
        self.font = font

    def GetPlayerName(self, input_reader):
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        idx = 0
        current_letter = letters[idx]
        pixel_offset = 70
        highscore_text = ["New High Score of " + str(self.score), "Type your name: "]
        done = False
        while not done:
            for event in pygame.event.get():
                action = input_reader.readInput(event)
                if action != None:
                    if action[1] == 'execute':
                        done = True
                    elif action[1] == 'up':
                        if(idx == len(letters) - 1):
                            idx = 0
                        else:
                            idx += 1
                        current_letter = letters[idx]
                    elif action[1] == 'down':
                        if (idx == 0):
                            idx = len(letters) - 1
                        else:
                            idx -= 1
                        current_letter = letters[idx]
                    elif action[1] == 'right':
                        self.name += current_letter
                    elif action[1] == 'left':
                        self.name = self.name[:len(self.name) - 1:]
            self.screen.fill(BLACK)

            for i in range(len(highscore_text)):
                rect = (((self.board_width - self.font.size(highscore_text[i])[0]) / 2), (
                    (self.board_height - self.font.size(highscore_text[i])[1] - pixel_offset) / 2) + i * pixel_offset)
                txt = self.font.render(highscore_text[i], 1, WHITE)
                self.screen.blit(txt, rect)

            text = self.font.render(self.name + current_letter, 1, WHITE)
            box_x = self.font.size(self.name + current_letter)[0]
            box_y = self.font.size(self.name + current_letter)[1]
            enter_box = pygame.Surface((box_x, box_y))
            text_position = ((self.board_width - box_x) / 2, rect[1] + pixel_offset)
            r = text.get_rect()
            enter_box.blit(text, r)
            self.screen.blit(enter_box, text_position)
            pygame.display.flip()
        return self.name