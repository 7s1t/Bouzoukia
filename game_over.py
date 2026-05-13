import pygame
import sys
from button import Button


class GameOverMenu:
    def __init__(self, screen, score, pb_score):
        self.screen = screen
        self.pb_score = pb_score
        self.score = score
        self.font = pygame.font.Font("icons/font.ttf", 54)
        self.font2 = pygame.font.Font("icons/font.ttf", 40)
        self.button_font = pygame.font.Font("icons/font.ttf", 32)
        self.menu_button = Button(self.scale_image('icons/Box.png', 160, 60),
                                  (self.screen.get_width() // 2, 400),
                                  "MENU", self.button_font, "White", "Yellow")
        self.quit_button = Button(self.scale_image('icons/Box.png', 160, 60),
                                  (screen.get_width() // 2, 500),
                                  "QUIT", self.button_font, "White", "Yellow")

    def show(self):
        pygame.mouse.set_visible(True)
        pygame.mixer.pause()
        self.paused = True

        while self.paused:
            self.screen.fill("#000000")
            game_over_text = self.font.render('Game Over', True, (255, 0, 0))
            score_text = self.font2.render(f"Score: {self.score}", True, (255, 255, 255))
            pb_score_text = self.font2.render(f"Pb Score: {self.pb_score}", True, (150, 255, 255))
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 100))
            self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, 200))
            self.screen.blit(pb_score_text, (self.screen.get_width() // 2 - pb_score_text.get_width() // 2, 280))
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.menu_button, self.quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.unpause()
                        return 'menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button.checkForInput(mouse_pos):
                        return 'menu'
                    if self.quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def scale_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height)).convert_alpha()
