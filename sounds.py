import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Load sounds
sounds = {
    'menu': pygame.mixer.Sound('sound/bouzoukia_game_menu_music.wav'),
    'mazonakis': pygame.mixer.Sound('sound/se_exo_kanei_theo.wav'),
    'karas': pygame.mixer.Sound('sound/kselogiastra.wav'),
    'mitropanos': pygame.mixer.Sound('sound/arxaggelos.wav')
}

# Manage sounds
class SoundManager:
    def __init__(self):
        self.sounds = sounds
        self.current_sound = None
        self.current_channel = None

    def play_menu_music(self):
        self.sounds['menu'].play(-1)
        self.current_sound = 'menu'

    def stop_menu_music(self):
        if self.current_sound == 'menu':
            self.sounds['menu'].stop()

    def play_game_music(self, player_number):
        self.stop_current_music()
        if player_number == 0:
            self.current_channel = self.sounds['karas'].play(-1)
            self.current_sound = 'karas'
        elif player_number == 1:
            self.current_channel = self.sounds['mazonakis'].play(-1)
            self.current_sound = 'mazonakis'
        elif player_number == 2:
            self.current_channel = self.sounds['mitropanos'].play(-1)
            self.current_sound = 'mitropanos'

    def stop_current_music(self):
        if self.current_sound:
            self.sounds[self.current_sound].stop()
            self.current_sound = None

    def pause_music(self):
        if self.current_channel:
            self.current_channel.pause()

    def unpause_music(self):
        if self.current_channel:
            self.current_channel.unpause()
