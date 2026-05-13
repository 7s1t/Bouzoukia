import pygame
import time
from button import Button
from icons import load_and_scale_icons
from menu import MainMenu


class SelectionMenu:
    def __init__(self, screen):
        self.screen = screen
        self.icons = load_and_scale_icons()
        self.font = pygame.font.Font("icons/font.ttf", 32)
        self.player_number = 0
        self.main_menu = MainMenu(screen)

        self.buttons = {
            'back': Button(pygame.transform.scale(pygame.image.load('icons/Box.png'), (160, 60)).convert_alpha(),
                           (self.screen.get_width() // 2, 580), "BACK", self.font, "Black", "Yellow")
        }
        self.player_rects = [
            self.icons['player'][0].get_rect(center=(280, 430)),
            self.icons['player'][1].get_rect(center=(480, 430)),
            self.icons['player'][2].get_rect(center=(680, 430))
        ]

    def show(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.icons['menu_bg'], (0, 0))
            choose_char_text = self.font.render("Choose your character", True, "Black")
            choose_char_rect = choose_char_text.get_rect(center=(self.screen.get_width() / 2, 55))
            self.screen.blit(choose_char_text, choose_char_rect)

            for i, rect in enumerate(self.player_rects):
                self.screen.blit(self.icons['player'][i], rect)

            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons.values():
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons['back'].checkForInput(mouse_pos):
                        return "back"
                    for i, rect in enumerate(self.player_rects):
                        if rect.collidepoint(event.pos):
                            self.player_number = i
                            return i

            pygame.display.update()
            time.sleep(0.01)
