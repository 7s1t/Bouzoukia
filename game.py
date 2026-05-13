import random
import sys
import os
import pygame
from menu import MainMenu
from pause_menu import PauseMenu
from icons import load_and_scale_icons
from sounds import SoundManager
from character_selection import SelectionMenu
from game_over import GameOverMenu
from gamemode import GameModeMenu

# Initialize Pygame
pygame.init()

screen_width = 320 * 3
screen_height = 208 * 3
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

pygame.display.set_caption("Terleguys")

icons = load_and_scale_icons()
sounds = SoundManager()

pygame.display.set_icon(icons['icon'])

scaled_background_icon = pygame.transform.scale(icons['background'], (screen_width, screen_height)).convert_alpha()


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.player_number = 0
        self.PB_SCORE = 'pb_score.txt'
        # Create the file with an initial score of 0 if it doesn't exist
        if not os.path.exists(self.PB_SCORE):
            with open(self.PB_SCORE, 'w') as file:
                file.write('0')
        self.pb_score = self.load_pb_score()
        self.playerX = 400
        self.playerY = 180
        self.player_target_x = self.playerX
        self.player_speed = 16
        self.player_positions = [180, 400, 620]
        self.current_position_index = 1
        self.enemies = []
        self.num_of_enemies = random.choices([1, 2], weights=[1, 2])[0]  # Generates a random number of enemies but not quite
        self.consecutive_same_count = 1
        self.last_enemy_count = self.num_of_enemies
        self.active_enemies = [True for _ in range(self.num_of_enemies)]
        self.enemy_speed = [2.2 for _ in range(self.num_of_enemies)]
        self.enemyX = []
        self.enemyY = [screen_height for _ in range(self.num_of_enemies)]
        self.flowerX = random.choice(self.enemyX) if self.enemyX else random.choice(self.player_positions)
        self.flowerY = random.choice([150, 350, 550])
        self.current_flower = [random.choice(icons['flower']) for _ in range(self.num_of_enemies)]
        self.flower_spawned = False
        self.current_screen = "menu"
        self.mode = 0
        self.font = pygame.font.Font("icons/font.ttf", 32)
        self.last_speed_increase_time = pygame.time.get_ticks()
        self.last_score_increase_time = pygame.time.get_ticks()

        for _ in range(self.num_of_enemies):
            new_x = random.choice(self.player_positions)
            while any(abs(new_x - x) < icons['player'][self.player_number].get_width() for x in self.enemyX):
                new_x = random.choice(self.player_positions)
            self.enemyX.append(new_x)

    def run(self):
        sounds.play_menu_music()
        while True:
            if self.current_screen == "menu":
                result = MainMenu(screen).show()
                self.health = 3
                self.score = 0
                self.playerX = 400
                self.current_position_index = 1
                self.player_target_x = 400
                self.enemy_speed = [2.2 for _ in range(self.num_of_enemies)]
                self.update_enemies()
                self.respawn_all_enemies()
                if result == 'play':
                    option = GameModeMenu(screen).show()
                    if isinstance(option, int):
                        self.mode = option
                        if self.mode == 0:
                            self.player_speed = 16
                        else:
                            self.player_speed = 26
                        self.current_screen = "selection_menu"
                elif result == 'options':
                    pass
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
            elif self.current_screen == "selection_menu":
                result = SelectionMenu(screen).show()
                self.current_screen = "selection_menu"
                if isinstance(result, int):
                    self.player_number = result
                    self.current_screen = "game"
                elif result == "back":
                    self.current_screen = "menu"
            elif self.current_screen == "game":
                sounds.stop_menu_music()
                sounds.play_game_music(self.player_number)
                self.play_game()
            elif self.current_screen == "resume":
                self.current_screen = "game"
                self.play_game()
            elif self.current_screen == "pause":
                result = PauseMenu(screen, self.pb_score).show()
                if result == 'menu':
                    sounds.stop_current_music()
                    self.current_screen = 'menu'
                    sounds.play_menu_music()
                elif result == 'back':
                    sounds.unpause_music()
                    self.current_screen = 'resume'
                print(self.current_screen)
            elif self.current_screen == "GameOverMenu":
                result = GameOverMenu(screen, self.score, self.pb_score).show()
                if result == 'menu':
                    self.current_screen = 'menu'
                    sounds.play_menu_music()

    def play_game(self):
        pygame.mouse.set_visible(False)
        running = True
        while running:
            screen.fill((0, 0, 0))
            screen.blit(scaled_background_icon, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_player(-1)
                    if event.key == pygame.K_RIGHT:
                        self.move_player(1)
                    if event.key == pygame.K_ESCAPE:
                        sounds.pause_music()
                        self.current_screen = "pause"
                        running = False

            # Player movement
            if self.playerX < self.player_target_x:
                self.playerX += min(self.player_speed, self.player_target_x - self.playerX)
            elif self.playerX > self.player_target_x:
                self.playerX -= min(self.player_speed, self.playerX - self.player_target_x)

            # Score
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_score_increase_time > 400) and (self.current_screen == 'game') and (self.mode == 0):
                self.score += 10
                self.last_score_increase_time = current_time
                if self.score > self.pb_score:
                    self.pb_score = self.score
                    with open(self.PB_SCORE, 'w') as file:
                        file.write(str(self.score))
            elif self.current_screen == 'menu':
                self.score = 0

            self.update_enemies()
            self.check_collisions()
            self.update_screen()

            self.clock.tick(60)

    def move_player(self, direction):
        new_index = self.current_position_index + direction
        if 0 <= new_index < len(self.player_positions):
            self.current_position_index = new_index
            self.player_target_x = self.player_positions[self.current_position_index]

    def update_enemies(self):
        current_time = pygame.time.get_ticks()
        for i in range(self.num_of_enemies):
            if self.active_enemies[i]:
                self.enemyY[i] -= self.enemy_speed[i]
                if self.enemyY[i] <= 100:
                    self.active_enemies[i] = False

        if all(not active for active in self.active_enemies):
            self.respawn_all_enemies()

        # Gradually increase enemy speed depending on the game mode
        if self.mode == 0:
            if (current_time - self.last_speed_increase_time > 6000) and (self.current_screen == 'game'):
                for i in range(self.num_of_enemies):
                    self.enemy_speed[i] += 0.3   # How much the speed will increase
                self.last_speed_increase_time = current_time
            elif self.current_screen == 'menu':
                self.enemy_speed = [2.2 for _ in range(self.num_of_enemies)]
        elif self.mode == 1:
            if (current_time - self.last_speed_increase_time > 4500) and (self.current_screen == 'game'):
                for i in range(self.num_of_enemies):
                    self.enemy_speed[i] += 0.5   # How much the speed will increase
                self.last_speed_increase_time = current_time
            elif self.current_screen == 'menu':
                self.enemy_speed = [2.2 for _ in range(self.num_of_enemies)]

    def respawn_all_enemies(self):
        self.randomize_enemy_count()
        for i in range(self.num_of_enemies):
            self.reset_enemy(i)
            self.active_enemies[i] = True  # Reactivate all enemies

    def reset_enemy(self, index):
        new_y = screen_height
        new_x = random.choice(self.player_positions)

        self.current_flower[index] = random.choice(icons['flower'])  # Assign a new random flower image

        while any(abs(new_x - self.enemyX[i]) < self.current_flower[index].get_width()
                  for i in range(self.num_of_enemies) if i != index):
            new_x = random.choice(self.player_positions)

        self.enemyY[index] = new_y
        self.enemyX[index] = new_x
        # self.enemy_speed[index] = max(self.enemy_speed)

    def randomize_enemy_count(self):
        choices = [1, 2]
        if self.consecutive_same_count >= 3:
            choices.remove(self.last_enemy_count)

        new_count = random.choice(choices)

        if new_count == self.last_enemy_count:
            self.consecutive_same_count += 1
        else:
            self.consecutive_same_count = 1
            self.last_enemy_count = new_count

        self.num_of_enemies = new_count

        while len(self.enemyX) < self.num_of_enemies:
            self.enemyX.append(random.choice(self.player_positions))
            self.enemyY.append(screen_height)
            self.enemy_speed.append(max(self.enemy_speed))
            self.active_enemies.append(True)
            self.current_flower.append(random.choice(icons['flower']))

        while len(self.enemyX) > self.num_of_enemies:
            self.enemyX.pop()
            self.enemyY.pop()
            self.enemy_speed.pop()
            self.active_enemies.pop()
            self.current_flower.pop()

    def check_collisions(self):
        player_rect = pygame.Rect(self.playerX, self.playerY, icons['player'][self.player_number].get_width(),
                                  icons['player'][self.player_number].get_height())

        for i in range(self.num_of_enemies):
            if self.active_enemies[i]:  # Only check active enemies
                enemy_rect = pygame.Rect(self.enemyX[i], self.enemyY[i], self.current_flower[i].get_width(),
                                         self.current_flower[i].get_height())
                if player_rect.colliderect(enemy_rect):
                    self.health -= 1
                    self.active_enemies[i] = False  # Set enemy as inactive
                if self.health <= 0:
                    sounds.stop_current_music()
                    pygame.mouse.set_visible(True)
                    self.current_screen = "GameOverMenu"
                    self.run()

    def load_pb_score(self):
        if os.path.exists(self.PB_SCORE):
            with open(self.PB_SCORE, 'r') as file:
                try:
                    score = int(file.read().strip())
                    return score
                except ValueError:
                    return 0  # If file is empty
        return 0  # If there hasn't been a pb score yet set it to 0

    def update_screen(self):
        screen.fill((0, 0, 0))
        screen.blit(scaled_background_icon, (0, 0))

        # Draw the player
        screen.blit(icons['player'][self.player_number], (self.playerX, self.playerY))

        # Draw the enemies
        for i in range(self.num_of_enemies):
            if self.active_enemies[i]:
                screen.blit(self.current_flower[i], (self.enemyX[i], self.enemyY[i]))

        # Display score and health
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        health_text = self.font.render(f"Health: {self.health}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))

        pygame.display.update()


if __name__ == "__main__":
    Game().run()
