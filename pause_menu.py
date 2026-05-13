import pygame
from button import Button


class PauseMenu:
    def __init__(self, screen, pb_score):
        self.screen = screen
        self.pb_score = pb_score
        self.font = pygame.font.Font("icons/font.ttf", 54)
        self.font2 = pygame.font.Font("icons/font.ttf", 40)
        self.button_font = pygame.font.Font("icons/font.ttf", 32)
        self.menu_button = Button(self.scale_image('icons/Box.png', 160, 60),
                                (self.screen.get_width() // 2, 330),
                                "MENU", self.button_font, "White", "Yellow")
        self.back_button = Button(self.scale_image('icons/Box.png', 160, 60),
                                (screen.get_width() // 2, 430),
                                "BACK", self.button_font, "White", "Yellow")

    def show(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.pause()
        self.paused = True

        while self.paused:
            self.screen.fill("#5D4C6E")
            # self.screen.fill("#FFFFFF")
            text = self.font.render('Paused', True, (255, 255, 255))
            pb_score_text = self.font2.render(f"Pb Score: {self.pb_score}", True, (150, 255, 255))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 100))
            self.screen.blit(pb_score_text, (self.screen.get_width() // 2 - pb_score_text.get_width() // 2, 200))
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.menu_button, self.back_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                        pygame.mixer.unpause()
                        return 'back'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button.checkForInput(mouse_pos):
                        return 'menu'
                    if self.back_button.checkForInput(mouse_pos):
                        self.paused = False
                        pygame.mixer.unpause()
                        return 'back'

            pygame.display.update()

    def scale_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height)).convert_alpha()
