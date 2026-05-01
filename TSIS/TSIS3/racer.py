import os
import random
import pygame

width = 400
height = 600
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (70, 70, 70)
dark_gray = (40, 40, 40)
yellow = (255, 215, 0)
orange = (255, 140, 0)
red = (220, 50, 50)
blue = (70, 140, 255)
green = (50, 220, 90)
purple = (170, 80, 255)
cyan = (70, 230, 255)

base_dir = os.path.dirname(__file__)
asset_dir = os.path.join(base_dir, "assets")
old_image_dir = os.path.join(base_dir, "images")

road_left = 80
road_right = width - 80
road_width = road_right - road_left
lanes = [100, 175, 250]
finish_distance = 3000

difficulty_data = {
    "easy": {"enemy_spawn": 105, "obstacle_spawn": 145, "speed": 4},
    "normal": {"enemy_spawn": 80, "obstacle_spawn": 115, "speed": 5},
    "hard": {"enemy_spawn": 55, "obstacle_spawn": 85, "speed": 6}
}

CAR_TINTS = {
    "blue": blue,
    "red": red,
    "green": green
}

pygame.mixer.init()

def load_image(name, size, fallback_color):
    for folder in (asset_dir, old_image_dir):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)
    image = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(image, fallback_color, image.get_rect(), border_radius=8)
    pygame.draw.rect(image, white, image.get_rect(), 2, border_radius=8)
    return image

def tint_image(image, color):
    result = image.copy()
    tint = pygame.Surface(result.get_size(), pygame.SRCALPHA)
    tint.fill((*color, 70))
    result.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return result

class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        base_image = load_image("player.png", (50, 90), blue)
        color = CAR_TINTS.get(settings.get("car_color", "blue"), blue)
        self.image = tint_image(base_image, color)
        self.rect = self.image.get_rect(center=(width // 2, height - 100))
        self.speed = 6
        self.shield = False
        self.repair = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if self.rect.left < road_left:
            self.rect.left = road_left
        if self.rect.right > road_right:
            self.rect.right = road_right

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = load_image("enemy.png", (50, 90), red)
        self.rect = self.image.get_rect(midtop=(random.choice(lanes), -120))
        self.speed = speed + random.randint(0, 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.weight = random.randint(1, 3)
        self.value = self.weight
        self.image = load_image("coin.png", (32, 32), yellow)
        if self.weight == 2:
            self.image = tint_image(self.image, orange)
        elif self.weight == 3:
            self.image = tint_image(self.image, red)
        self.rect = self.image.get_rect(center=(random.choice(lanes), -40))
        self.speed = speed
        self.life = fps * 6

    def update(self):
        self.rect.y += self.speed
        self.life -= 1
        if self.rect.top > height or self.life <= 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
        self.speed = speed
        self.image = pygame.Surface((55, 35), pygame.SRCALPHA)
        if self.kind == "barrier":
            pygame.draw.rect(self.image, orange, self.image.get_rect(), border_radius=5)
            pygame.draw.line(self.image, white, (5, 5), (50, 30), 4)
        elif self.kind == "oil":
            pygame.draw.ellipse(self.image, black, self.image.get_rect())
            pygame.draw.ellipse(self.image, dark_gray, (8, 7, 35, 20))
        elif self.kind == "pothole":
            pygame.draw.ellipse(self.image, dark_gray, self.image.get_rect())
            pygame.draw.ellipse(self.image, black, (8, 6, 35, 22))
        else:
            pygame.draw.rect(self.image, yellow, self.image.get_rect(), border_radius=5)
            pygame.draw.line(self.image, black, (0, 15), (55, 15), 3)
        self.rect = self.image.get_rect(center=(random.choice(lanes), -50))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        if self.kind == "nitro":
            color = cyan
            letter = "N"
        elif self.kind == "shield":
            color = purple
            letter = "S"
        else:
            color = green
            letter = "R"
        pygame.draw.circle(self.image, color, (18, 18), 18)
        pygame.draw.circle(self.image, white, (18, 18), 18, 2)
        font = pygame.font.SysFont("Verdana", 20, bold=True)
        text = font.render(letter, True, white)
        self.image.blit(text, text.get_rect(center=(18, 18)))
        self.rect = self.image.get_rect(center=(random.choice(lanes), -45))
        self.speed = speed
        self.life = fps * 5

    def update(self):
        self.rect.y += self.speed
        self.life -= 1
        if self.rect.top > height or self.life <= 0:
            self.kill()

class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((70, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.image, red, self.image.get_rect(), border_radius=6)
        pygame.draw.line(self.image, white, (5, 6), (65, 24), 4)
        self.rect = self.image.get_rect(center=(width // 2, -70))
        self.speed = speed
        self.dx = random.choice([-2, 2])

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.dx
        if self.rect.left < road_left or self.rect.right > road_right:
            self.dx *= -1
        if self.rect.top > height:
            self.kill()

class RacerGame:
    def __init__(self, screen, clock, username, settings):
        self.screen = screen
        self.clock = clock
        self.username = username
        self.settings = settings
        self.font = pygame.font.SysFont("Verdana", 18)
        self.big_font = pygame.font.SysFont("Verdana", 32, bold=True)
        self.road_img = self.load_road()
        self.crash_sound = pygame.mixer.Sound(os.path.join(asset_dir, "crash.wav"))
        self.money_sound = pygame.mixer.Sound(os.path.join(asset_dir, "money.wav"))
        self.reset()

    def load_road(self):
        for folder in (asset_dir, old_image_dir):
            path = os.path.join(folder, "road.png")
            if os.path.exists(path):
                image = pygame.image.load(path).convert()
                return pygame.transform.scale(image, (width, height))
        return None

    def reset(self):
        self.player = Player(self.settings)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemies = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.events = pygame.sprite.Group()
        self.coins = 0
        self.score = 0
        self.distance = 0
        self.game_over = False
        self.finished = False
        self.saved = False
        self.enemy_timer = 0
        self.coin_timer = 0
        self.obstacle_timer = 0
        self.powerup_timer = 0
        self.event_timer = 0
        self.active_power = None
        self.power_time = 0
        self.nitro_bonus = 0

    def difficulty(self):
        return difficulty_data.get(self.settings.get("difficulty", "normal"), difficulty_data["normal"])

    def current_speed(self):
        level_bonus = int(self.distance // 700)
        return self.difficulty()["speed"] + level_bonus + self.nitro_bonus

    def safe_to_spawn(self, x):
        return abs(self.player.rect.centerx - x) > 45 or self.player.rect.y < height - 180

    def spawn_enemy(self):
        speed = self.current_speed()
        enemy = Enemy(speed)
        if self.safe_to_spawn(enemy.rect.centerx):
            self.enemies.add(enemy)

    def spawn_obstacle(self):
        obstacle = Obstacle(self.current_speed())
        if self.safe_to_spawn(obstacle.rect.centerx):
            self.obstacles.add(obstacle)

    def update_timers(self):
        speed = self.current_speed()
        difficulty = self.difficulty()
        progress_bonus = int(self.distance // 600) * 4
        self.enemy_timer += 1
        if self.enemy_timer >= max(25, difficulty["enemy_spawn"] - progress_bonus):
            self.enemy_timer = 0
            self.spawn_enemy()
        self.coin_timer += 1
        if self.coin_timer >= 70:
            self.coin_timer = 0
            self.coins_group.add(Coin(speed))
        self.obstacle_timer += 1
        if self.obstacle_timer >= max(35, difficulty["obstacle_spawn"] - progress_bonus):
            self.obstacle_timer = 0
            self.spawn_obstacle()
        self.powerup_timer += 1
        if self.powerup_timer >= 360:
            self.powerup_timer = 0
            if len(self.powerups) == 0 and self.active_power is None:
                self.powerups.add(PowerUp(speed))
        self.event_timer += 1
        if self.event_timer >= 500:
            self.event_timer = 0
            self.events.add(MovingBarrier(speed))

    def collect_items(self):
        coins = pygame.sprite.spritecollide(self.player, self.coins_group, True)
        for coin in coins:
            self.coins += coin.value
            self.score += coin.value * 10
            self.money_sound.play()
        powerups = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerups:
            if self.active_power is None:
                self.active_power = powerup.kind
                if powerup.kind == "nitro":
                    self.power_time = fps * 4
                    self.nitro_bonus = 4
                    self.score += 30
                elif powerup.kind == "shield":
                    self.player.shield = True
                    self.power_time = 0
                    self.score += 20
                elif powerup.kind == "repair":
                    self.player.repair += 1
                    self.active_power = None
                    self.score += 15
                    if len(self.obstacles) > 0:
                        self.obstacles.sprites()[0].kill()

    def handle_power_timer(self):
        if self.active_power == "nitro":
            self.power_time -= 1
            if self.power_time <= 0:
                self.active_power = None
                self.nitro_bonus = 0

    def handle_collision_group(self, group):
        hit = pygame.sprite.spritecollideany(self.player, group)
        if not hit:
            return
        if self.player.shield:
            hit.kill()
            self.player.shield = False
            self.active_power = None
            return
        if self.player.repair > 0:
            hit.kill()
            self.player.repair -= 1
            return
        self.crash_sound.play()
        self.game_over = True

    def update(self):
        if self.game_over or self.finished:
            return
        self.player_group.update()
        self.enemies.update()
        self.coins_group.update()
        self.obstacles.update()
        self.powerups.update()
        self.events.update()
        self.update_timers()
        self.collect_items()
        self.handle_power_timer()
        self.handle_collision_group(self.enemies)
        self.handle_collision_group(self.obstacles)
        self.handle_collision_group(self.events)
        self.distance += self.current_speed() / 5
        self.score += 1
        if self.distance >= finish_distance:
            self.finished = True
            self.score += 500

    def draw_road(self):
        if self.road_img:
            self.screen.blit(self.road_img, (0, 0))
        else:
            self.screen.fill((45, 45, 45))
            pygame.draw.rect(self.screen, (35, 35, 35), (road_left, 0, road_width, height))
            pygame.draw.line(self.screen, white, (road_left, 0), (road_left, height), 3)
            pygame.draw.line(self.screen, white, (road_right, 0), (road_right), 3)
            for y in range(0, height, 80):
                pygame.draw.line(self.screen, white, (width // 2, y), (width // 2, y + 40), 3)

    def draw_hud(self):
        remaining = max(0, int(finish_distance - self.distance))
        texts = [
            f"Score: {self.score}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)}m",
            f"Finish: {remaining}m"
        ]
        y = 10
        for text in texts:
            surface = self.font.render(text, True, white)
            self.screen.blit(surface, (10, y))
            y += 24
        power_text = "Power: none"
        if self.active_power == "nitro":
            power_text = f"Power: nitro {self.power_time // fps + 1}s"
        elif self.player.shield:
            power_text = "Power: shield"
        elif self.player.repair > 0:
            power_text = f"Repair: {self.player.repair}"
        surface = self.font.render(power_text, True, yellow)
        self.screen.blit(surface, (10, y))

    def draw(self):
        self.draw_road()
        self.coins_group.draw(self.screen)
        self.powerups.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.events.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player_group.draw(self.screen)
        self.draw_hud()
        if self.player.shield:
            pygame.draw.circle(self.screen, cyan, self.player.rect.center, 55, 3)
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
            self.update()
            self.draw()
            if self.game_over:
                return "game_over"
            if self.finished:
                return "finished"