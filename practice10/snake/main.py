import pygame
import random

snake_speed = 10
level = 1

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(255, 255, 0)

pygame.init()

pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

def generate_food():
    global fruit_position, fruit_weight, fruit_color, food_timer
    fruit_position = [random.randrange(1, (window_x//10)) * 10,
                      random.randrange(1, (window_y//10)) * 10]
    fruit_weight = random.randint(1, 3)
    if fruit_weight == 1:
        fruit_color = white
        food_timer = 300
    elif fruit_weight == 2:
        fruit_color = yellow
        food_timer = 240
    else:
        fruit_color = red
        food_timer = 180

def reset_game():
    global snake_position, snake_body, fruit_position
    global fruit_spawn, direction, change_to, score
    global level, snake_speed
    global fruit_weight, fruit_color, food_timer
    
    snake_position = [100, 50]
    snake_body = [[100, 50],[90, 50],[80, 50],[70, 50]]
    generate_food()
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    level = 1
    snake_speed = 10

reset_game()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    
    score_surface = score_font.render('Score: ' + str(score), True, color)
    level_surface = score_font.render('Level: ' + str(level), True, color)
    weight_surface = score_font.render('Food: ' + str(fruit_weight), True, color)
    timer_surface = score_font.render('Timer: ' + str(food_timer // snake_speed), True, color)

    y = window_y - 80
    game_window.blit(score_surface, (10, y))
    game_window.blit(level_surface, (10, y + 20))
    game_window.blit(weight_surface, (200, y))
    game_window.blit(timer_surface, (200, y + 20))

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    restart_font = pygame.font.SysFont('times new roman', 25)
    
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    restart_surface = restart_font.render('Press R to restart or Q to quit', True, white)
    game_over_surface_level = my_font.render('Your Level is : ' + str(level), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    restart_rect = restart_surface.get_rect()
    game_over_surface_level_rect = game_over_surface_level.get_rect()

    game_over_rect.midtop = (window_x//2, 120)
    restart_rect.midtop = (window_x//2, 240)
    game_over_surface_level_rect.midtop = (window_x//2, 160)

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
    snake_speed = 10 + (level - 1) * 2
    
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

    snake_body.insert(0, list(snake_position))

    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += fruit_weight * 10
        fruit_spawn = False
    else:
        snake_body.pop()
        
    food_timer -= 1

    if food_timer <= 0:
        fruit_spawn = False
        
    if not fruit_spawn:
        generate_food()
        
    fruit_spawn = True

    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, fruit_color, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

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