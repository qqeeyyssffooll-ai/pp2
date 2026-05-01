# Imports
import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# FPS settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_ROAD = (15, 15, 15)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 130, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)

# Screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Road settings
ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Object sizes
CAR_WIDTH = 80
COIN_SIZE = 32

# Game variables
SPEED = 5
MONEY_SCORE = 0
NEXT_SPEED_SCORE = 10
road_offset = 0

# Create game window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Load images
icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(icon)

# Load coin images
bronze_coin = pygame.image.load("image/bronze_coin.png")
silver_coin = pygame.image.load("image/silver_coin.png")
gold_coin = pygame.image.load("image/golden_coin.png")

bronze_coin = pygame.transform.scale(bronze_coin, (COIN_SIZE, COIN_SIZE))
silver_coin = pygame.transform.scale(silver_coin, (COIN_SIZE, COIN_SIZE))
gold_coin = pygame.transform.scale(gold_coin, (COIN_SIZE, COIN_SIZE))

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Load sounds
background_sound = pygame.mixer.Sound("sound/JENNIE_BLACKPINK_Tame_Impala_-_Dracula_Remix_(SkySound.cc).mp3")
crash_sound = pygame.mixer.Sound("sound/crash.wav")
coin_sound = pygame.mixer.Sound("sound/lost_money.wav")

# Play background sound in loop
background_sound.play(-1)


# Resize image without changing its proportions
def resize_by_width(image, new_width):
    old_width = image.get_width()
    old_height = image.get_height()
    new_height = int(old_height * new_width / old_width)
    return pygame.transform.smoothscale(image, (new_width, new_height))


# Draw moving road
def draw_road(surface, offset):
    # Draw green background around the road
    surface.fill(GREEN)

    # Draw gray road shoulders
    pygame.draw.rect(surface, GRAY, (ROAD_LEFT - 15, 0, ROAD_WIDTH + 30, SCREEN_HEIGHT))

    # Draw main black road
    pygame.draw.rect(surface, DARK_ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    # Draw white side border lines
    pygame.draw.line(surface, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 4)
    pygame.draw.line(surface, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 4)

    # Draw extra gray side details
    pygame.draw.line(surface, LIGHT_GRAY, (ROAD_LEFT - 10, 0), (ROAD_LEFT - 10, SCREEN_HEIGHT), 3)
    pygame.draw.line(surface, LIGHT_GRAY, (ROAD_RIGHT + 10, 0), (ROAD_RIGHT + 10, SCREEN_HEIGHT), 3)

    # Draw moving dashed center line
    line_width = 8
    line_height = 60
    gap = 80
    line_x = SCREEN_WIDTH // 2 - line_width // 2

    for y in range(-line_height, SCREEN_HEIGHT + gap, line_height + gap):
        pygame.draw.rect(
            surface,
            WHITE,
            (line_x, y + offset, line_width, line_height)
        )


# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Coins have different images and different weights
        self.types = [
            {"image": bronze_coin, "value": 1},
            {"image": silver_coin, "value": 2},
            {"image": gold_coin, "value": 3}
        ]

        # Choose random coin type
        self.change_type()

        self.rect = self.image.get_rect()

        # Coin appears randomly on the road
        self.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), 0)

    def change_type(self):
        # Randomly choose coin image and value
        current_type = random.choice(self.types)
        self.image = current_type["image"]
        self.value = current_type["value"]

    def move(self):
        # Move coin down
        self.rect.move_ip(0, SPEED)

        # If coin leaves the screen, move it back to the top and change type
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), 0)
            self.change_type()


# Enemy car class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and resize enemy car without distortion
        original_image = pygame.image.load("image/Enemy.png").convert_alpha()
        self.image = resize_by_width(original_image, CAR_WIDTH)
        self.rect = self.image.get_rect()

        # Enemy appears randomly on the road
        self.rect.center = (random.randint(ROAD_LEFT + 40, ROAD_RIGHT - 40), 0)

    def move(self):
        # Move enemy down
        self.rect.move_ip(0, SPEED)

        # If enemy leaves the screen, return it to the top
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(ROAD_LEFT + 40, ROAD_RIGHT - 40), 0)


# Player car class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and resize player car without distortion
        original_image = pygame.image.load("image/Player.png").convert_alpha()
        self.image = resize_by_width(original_image, CAR_WIDTH)
        self.rect = self.image.get_rect()

        # Player starting position
        self.rect.center = (SCREEN_WIDTH // 2, 520)

    def move(self):
        # Get pressed keys
        pressed_keys = pygame.key.get_pressed()

        # Move left, but do not leave the road
        if self.rect.left > ROAD_LEFT:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # Move right, but do not leave the road
        if self.rect.right < ROAD_RIGHT:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Create objects
P1 = Player()
E1 = Enemy()
M1 = Coin()

# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

money = pygame.sprite.Group()
money.add(M1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(M1)


# Main game loop
while True:
    # Check all events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Increase enemy speed when player earns enough coins
    if MONEY_SCORE >= NEXT_SPEED_SCORE:
        SPEED += 2
        NEXT_SPEED_SCORE += 10

    # Move road lines
    road_offset += SPEED

    # Reset road animation offset
    if road_offset >= 140:
        road_offset = 0

    # Draw moving road
    draw_road(DISPLAYSURF, road_offset)

    # Move and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Create smaller hitboxes for better collision
    # This prevents game over when cars are only visually near each other
    player_hitbox = P1.rect.inflate(-45, -45)
    enemy_hitbox = E1.rect.inflate(-45, -45)

    # Check collision between player and enemy using smaller hitboxes
    if player_hitbox.colliderect(enemy_hitbox):
        background_sound.stop()
        crash_sound.play()

        time.sleep(0.5)

        waiting = True

        # Game over screen with restart and quit options
        while waiting:
            DISPLAYSURF.fill(RED)

            DISPLAYSURF.blit(game_over_text, (30, 230))

            score_text = font_small.render("Score: " + str(MONEY_SCORE), True, BLACK)
            DISPLAYSURF.blit(score_text, (140, 320))

            restart_text = font_small.render("R - Restart", True, BLACK)
            DISPLAYSURF.blit(restart_text, (140, 500))

            quit_text = font_small.render("Q - Quit", True, BLACK)
            DISPLAYSURF.blit(quit_text, (140, 525))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart game variables
                        waiting = False
                        MONEY_SCORE = 0
                        SPEED = 5
                        NEXT_SPEED_SCORE = 10

                        # Reset enemy position
                        E1.rect.top = 0
                        E1.rect.center = (random.randint(ROAD_LEFT + 40, ROAD_RIGHT - 40), 0)

                        # Reset coin position and type
                        M1.rect.top = 0
                        M1.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), 0)
                        M1.change_type()

                        # Start music again
                        background_sound.play(-1)

                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    # Check collision between player and coin
    if pygame.sprite.spritecollideany(P1, money):
        coin_sound.play()

        # Increase score depending on coin weight
        MONEY_SCORE += M1.value

        # Return coin to random top position and change its type
        M1.rect.top = 0
        M1.rect.center = (random.randint(ROAD_LEFT + 30, ROAD_RIGHT - 30), 0)
        M1.change_type()

    # Show collected coins in the top right corner
    coin_text = font_small.render("Coins: " + str(MONEY_SCORE), True, YELLOW)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 130, 15))

    # Show current speed
    speed_text = font_small.render("Speed: " + str(SPEED), True, YELLOW)
    DISPLAYSURF.blit(speed_text, (SCREEN_WIDTH - 130, 40))

    # Show coin values on the left side
    DISPLAYSURF.blit(bronze_coin, (10, 40))
    DISPLAYSURF.blit(silver_coin, (10, 75))
    DISPLAYSURF.blit(gold_coin, (10, 110))

    bronze_text = font_small.render("= 1", True, YELLOW)
    silver_text = font_small.render("= 2", True, YELLOW)
    gold_text = font_small.render("= 3", True, YELLOW)

    DISPLAYSURF.blit(bronze_text, (45, 45))
    DISPLAYSURF.blit(silver_text, (45, 80))
    DISPLAYSURF.blit(gold_text, (45, 115))

    # Update display
    pygame.display.update()

    # Control FPS
    FramePerSec.tick(FPS)