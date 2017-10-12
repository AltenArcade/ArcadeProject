import pygame

BLACK = (0, 0, 0)

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color):
        super().__init__()
        self.block_size = size
        self.image = pygame.Surface([self.block_size, self.block_size])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        pygame.draw.rect(self.image, color, [0, 0, size, size])

    def update(self, action):
        if action == "down":
            self.rect.y += self.block_size
        if action == "left":
            self.rect.x -= self.block_size
        if action == "right":
            self.rect.x += self.block_size
        if action == "reset down":
            self.rect.y -= self.block_size
        if action == "reset right":
            self.rect.x -= self.block_size
        if action == "reset left":
            self.rect.x += self.block_size

    def Draw(self, color):
        pygame.draw.rect(self.image, color, [0, 0, self.block_size, self.block_size])