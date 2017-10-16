class Option:
    hovered = False

    def __init__(self, text, pos, screen, font, color_hov, color):
        self.screen = screen
        self.font = font
        self.text = text
        self.pos = pos
        self.color_hovered = color_hov
        self.color = color
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        self.screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return self.color_hovered
        else:
            return self.color

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos