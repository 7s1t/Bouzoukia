import pygame
import sys


# Load and scale icons
def load_and_scale_icons():
    icons = {
        'icon': pygame.image.load('icons/sakura.png'),
        'background': pygame.image.load('icons/background_2.png'),
        'menu_bg': pygame.image.load("icons/logo_1.png"),
        'player': [
            pygame.image.load('icons/karras_1.png'),
            pygame.image.load('icons/mazonakis_1.png'),
            pygame.image.load('icons/mitropanos_1.png'),
        ],
        'flower': [
            pygame.image.load('icons/flower_red.png'),
            pygame.image.load('icons/flower_yellow.png'),
            pygame.image.load('icons/flower_blue.png')
        ]
    }

    # Scale menu_bg
    icons['menu_bg'] = pygame.transform.scale(icons['menu_bg'], (960, 627))

    # Scale player images
    icons['player'] = [pygame.transform.scale(img, (
        int(img.get_width() * 0.7), int(img.get_height() * 0.7))) for img in icons['player']]

    # Scale flower images
    try:
        icons['flower'] = [pygame.transform.scale(img, (
            int(img.get_width() * 0.6), int(img.get_height() * 0.6))) for img in icons['flower']]
    except pygame.error as icons_error:
        print(f"Error loading image: {icons_error}")
        pygame.quit()
        sys.exit()

    return icons
