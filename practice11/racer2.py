import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()
pygame.mixer.init()

fps = 60
FramePerSec = pygame.time.Clock()

red = (255, 0, 0)
black = (0, 0, 0)
dark_road = (15, 15, 15)
white = (255, 255, 255)
yellow = (255, 255, 0)
green = (0, 130, 0)
gray = (100, 100, 100)
light_gray = (180, 180, 180)

screen_width = 400
screen_height = 600

road_left = 50
road_right = 350
road_width = road_right - road_left

car_width = 80
coin_size = 32

speed = 5
money_score = 0
next_speed_score = 10
road_offset = 0

displaysurf = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racer")

icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(icon)

bronze_coin = pygame.image.load("image/bronze_coin.png")
silver_coin = pygame.image.load("image/silver_coin.png")
gold_coin = pygame.image.load("image/golden_coin.png")

bronze_coin = pygame.transform.scale(bronze_coin, (coin_size, coin_size))
silver_coin = pygame.transform.scale(silver_coin, (coin_size, coin_size))
gold_coin = pygame.transform.scale(gold_coin, (coin_size, coin_size))

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, black)

background_sound = pygame.mixer.Sound("sound/JENNIE_blackPINK_Tame_Impala_-_Dracula_Remix_(SkySound.cc).mp3")
crash_sound = pygame.mixer.Sound("sound/crash.wav")
coin_sound = pygame.mixer.Sound("sound/lost_money.wav")

background_sound.play(-1)

def resize_by_width(image, new_width):
    old_width = image.get_width()
    old_height = image.get_height()
    new_height = int(old_height * new_width / old_width)
    return pygame.transform.smoothscale(image, (new_width, new_height))

def draw_road(surface, offset):
    surface.fill(green)

    pygame.draw.rect(surface, gray, (road_left - 15, 0, road_width + 30, screen_height))

    pygame.draw.rect(surface, dark_road, (road_left, 0, road_width, screen_height))

    pygame.draw.line(surface, white, (road_left, 0), (road_left, screen_height), 4)
    pygame.draw.line(surface, white, (road_right, 0), (road_right, screen_height), 4)

    pygame.draw.line(surface, light_gray, (road_left - 10, 0), (road_left - 10, screen_height), 3)
    pygame.draw.line(surface, light_gray, (road_right + 10, 0), (road_right + 10, screen_height), 3)

    line_width = 8
    line_height = 60
    gap = 80
    line_x = screen_width // 2 - line_width // 2

    for y in range(-line_height, screen_height + gap, line_height + gap):
        pygame.draw.rect(
            surface,
            white,
            (line_x, y + offset, line_width, line_height)
        )

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.types = [
            {"image": bronze_coin, "value": 1},
            {"image": silver_coin, "value": 2},
            {"image": gold_coin, "value": 3}
        ]

        self.change_type()

        self.rect = self.image.get_rect()

        self.rect.center = (random.randint(road_left + 30, road_right - 30), 0)

    def change_type(self):
        current_type = random.choice(self.types)
        self.image = current_type["image"]
        self.value = current_type["value"]

    def move(self):
        self.rect.move_ip(0, speed)

        if self.rect.top > screen_height:
            self.rect.top = 0
            self.rect.center = (random.randint(road_left + 30, road_right - 30), 0)
            self.change_type()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        original_image = pygame.image.load("image/Enemy.png").convert_alpha()
        self.image = resize_by_width(original_image, car_width)
        self.rect = self.image.get_rect()

        self.rect.center = (random.randint(road_left + 40, road_right - 40), 0)

    def move(self):
        self.rect.move_ip(0, speed)

        if self.rect.top > screen_height:
            self.rect.top = 0
            self.rect.center = (random.randint(road_left + 40, road_right - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        original_image = pygame.image.load("image/Player.png").convert_alpha()
        self.image = resize_by_width(original_image, car_width)
        self.rect = self.image.get_rect()

        self.rect.center = (screen_width // 2, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > road_left:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < road_right:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

p1 = Player()
e1 = Enemy()
m1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(e1)

money = pygame.sprite.Group()
money.add(m1)

all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(e1)
all_sprites.add(m1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if money_score >= next_speed_score:
        speed += 2
        next_speed_score += 10

    road_offset += speed

    if road_offset >= 140:
        road_offset = 0

    draw_road(displaysurf, road_offset)

    for entity in all_sprites:
        displaysurf.blit(entity.image, entity.rect)
        entity.move()

    player_hitbox = p1.rect.inflate(-45, -45)
    enemy_hitbox = e1.rect.inflate(-45, -45)

    if player_hitbox.colliderect(enemy_hitbox):
        background_sound.stop()
        crash_sound.play()

        time.sleep(0.5)

        waiting = True

        while waiting:
            displaysurf.fill(red)

            displaysurf.blit(game_over_text, (30, 230))

            score_text = font_small.render("Score: " + str(money_score), True, black)
            displaysurf.blit(score_text, (140, 320))

            restart_text = font_small.render("R - Restart", True, black)
            displaysurf.blit(restart_text, (140, 500))

            quit_text = font_small.render("Q - Quit", True, black)
            displaysurf.blit(quit_text, (140, 525))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        money_score = 0
                        speed = 5
                        next_speed_score = 10

                        # Reset enemy position
                        e1.rect.top = 0
                        e1.rect.center = (random.randint(road_left + 40, road_right - 40), 0)

                        m1.rect.top = 0
                        m1.rect.center = (random.randint(road_left + 30, road_right - 30), 0)
                        m1.change_type()

                        background_sound.play(-1)

                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    if pygame.sprite.spritecollideany(p1, money):
        coin_sound.play()

        money_score += m1.value

        m1.rect.top = 0
        m1.rect.center = (random.randint(road_left + 30, road_right - 30), 0)
        m1.change_type()

    coin_text = font_small.render("Coins: " + str(money_score), True, yellow)
    displaysurf.blit(coin_text, (screen_width - 130, 15))

    speed_text = font_small.render("speed: " + str(speed), True, yellow)
    displaysurf.blit(speed_text, (screen_width - 130, 40))

    displaysurf.blit(bronze_coin, (10, 40))
    displaysurf.blit(silver_coin, (10, 75))
    displaysurf.blit(gold_coin, (10, 110))

    bronze_text = font_small.render("= 1", True, yellow)
    silver_text = font_small.render("= 2", True, yellow)
    gold_text = font_small.render("= 3", True, yellow)

    displaysurf.blit(bronze_text, (45, 45))
    displaysurf.blit(silver_text, (45, 80))
    displaysurf.blit(gold_text, (45, 115))

    pygame.display.update()

    FramePerSec.tick(fps)