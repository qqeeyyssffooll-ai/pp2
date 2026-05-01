import pygame
import random

snake_speed = 15
level = 1

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

food_types = [
    {"color": red, "value": 10},  
    {"color": yellow, "value": 20},  
    {"color": blue, "value": 30}    
]

pygame.init()

pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

food_lifetime = 5000
food_spawn_time = 0

def spawn_food():
    food_type = random.choice(food_types)
    return {
        "position": [random.randrange(1, (window_x//10)) * 10,
                     random.randrange(1, (window_y//10)) * 10],
        "color": food_type["color"],
        "value": food_type["value"]
    }

def reset_game():
    global snake_position, snake_body
    global fruit_spawn, direction, change_to, score
    global level, snake_speed
    global current_food, food_spawn_time
    
    snake_position = [100, 50]

    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]

    current_food = spawn_food()
    food_spawn_time = pygame.time.get_ticks()
    
    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0
    level = 1
    snake_speed = 15


reset_game()

def show_score(choice, color, font, size):
  
    score_font = pygame.font.SysFont(font, size)
    
    score_surface = score_font.render('Score : ' + str(score), True, color)
    
    score_rect = score_surface.get_rect()
    
    game_window.blit(score_surface, score_rect)
    
    level_font = pygame.font.SysFont(font, size)
    level_surface = level_font.render('Level : ' + str(level), True, color)
    game_window.blit(level_surface, (1, 18))
    
    timer_surface = score_font.render('Timer : ' + str(time_left), True, color)
    game_window.blit(timer_surface, (1, 100))    
    
    for index, food in enumerate(food_types):
        y = 45 + index * 22
        pygame.draw.rect(game_window, food["color"], pygame.Rect(5, y, 12, 12))
        
        value_surface = score_font.render(str(food["value"]), True, white)
        game_window.blit(value_surface, (24, y - 6))
        
        dop_surface = score_font.render("-", True, white)
        game_window.blit(dop_surface, (17, y - 8))

def game_over():
    
    my_font = pygame.font.SysFont('times new roman', 50)
    restart_font = pygame.font.SysFont('times new roman', 25)

    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    restart_surface = restart_font.render(
        'Press R to restart or Q to quit', True, white)

    game_over_surface_level= my_font.render(
        'Your Level is : ' + str(level), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    restart_rect = restart_surface.get_rect()
    game_over_surface_level_rect = game_over_surface_level.get_rect()
    game_over_rect.midtop = (360, 120)
    restart_rect.midtop = (360, 240)
    game_over_surface_level_rect.midtop = (360, 160)

    while True:
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        game_window.blit(restart_surface, restart_rect)
        game_window.blit(game_over_surface_level, game_over_surface_level_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        fps.tick(15)

while True:
    
    level = score // 30 + 1
    snake_speed = 15 + (level - 1) * 5

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    current_time = pygame.time.get_ticks()

    time_left = max(0, food_lifetime - (current_time - food_spawn_time)) // 1000

    if current_time - food_spawn_time >= food_lifetime:
        current_food = spawn_food()
        food_spawn_time = current_time

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == current_food["position"][0] and snake_position[1] == current_food["position"][1]:
        score += current_food["value"]
        fruit_spawn = False
        food_spawn_time = pygame.time.get_ticks()
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        current_food = spawn_food()
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, current_food["color"], pygame.Rect(
        current_food["position"][0], current_food["position"][1], 10, 10))
    
    game_over_triggered = False
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over_triggered = True
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over_triggered = True

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over_triggered = True
            break

    if game_over_triggered:
        game_over()
        continue

    show_score(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)