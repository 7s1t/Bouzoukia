import pygame
from button import Button


class GameModeMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("icons/font.ttf", 54)
        self.button_font = pygame.font.Font("icons/font.ttf", 32)
        self.a_button = Button(self.scale_image('icons/Box.png', 220, 60),
                                  (self.screen.get_width() // 2, 300),
                                  "NORMAL", self.button_font, "White", "Blue")
        self.b_button = Button(self.scale_image('icons/Box.png', 160, 60),
                                  (self.screen.get_width() // 2, 400),
                                  "RUSH", self.button_font, "White", "Red")

    def show(self):
        pygame.mouse.set_visible(True)

        while True:
            self.screen.fill("#5D4C6E")
            text = self.font.render('Choose gamemode', True, (0, 0, 0))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 110))
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.a_button, self.b_button,]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.a_button.checkForInput(mouse_pos):
                        mode = 0
                        return mode
                    if self.b_button.checkForInput(mouse_pos):
                        mode = 1
                        return mode

            pygame.display.update()

    def scale_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height)).convert_alpha()
