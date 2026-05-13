import pygame
import sys
import time
from button import Button
from icons import load_and_scale_icons
from sounds import SoundManager


class MainMenu:

    def __init__(self, screen):
        self.screen = screen
        self.icons = load_and_scale_icons()
        self.sounds = SoundManager()

        # Profile load_and_scale_icons
        start_time = time.time()
        self.icons = load_and_scale_icons()
        print(f"Time to load and scale icons: {time.time() - start_time:.2f} seconds")

        # Profile load_sounds
        start_time = time.time()
        self.sounds = SoundManager()
        print(f"Time to load sounds: {time.time() - start_time:.2f} seconds")

        self.font = pygame.font.Font("icons/font.ttf", 32)
        self.buttons = {
            'play': Button(self.scale_image('icons/Box.png', 160, 60),
                           (self.screen.get_width() // 2, 350),
                           "PLAY", self.font, "#d7fcd4", "yellow"),
            'options': Button(self.scale_image('icons/Box.png', 250, 60),
                              (self.screen.get_width() // 2, 440),
                              "OPTIONS", self.font, "#d7fcd4", "yellow"),
            'quit': Button(self.scale_image('icons/Box.png', 160, 60),
                           (self.screen.get_width() // 2, 530),
                           "QUIT", self.font, "#d7fcd4", "yellow")
        }

    def scale_image(self, path, width, height):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (width, height)).convert_alpha()

    def show(self):
        while True:
            self.screen.blit(self.icons['menu_bg'], (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons.values():
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons['play'].checkForInput(mouse_pos):
                        # Start the game
                        return 'play'
                    if self.buttons['options'].checkForInput(mouse_pos):
                        # Show options menu
                        return 'options'
                    if self.buttons['quit'].checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            time.sleep(0.01)
