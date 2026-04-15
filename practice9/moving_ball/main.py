import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()

x = 600
y = 300

done = False

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]: y -= 20
    if pressed[pygame.K_DOWN]: y += 20
    if pressed[pygame.K_LEFT]: x -= 20
    if pressed[pygame.K_RIGHT]: x += 20

    if x < 25:
        x = 25
    if x > 1200 - 25:
        x = 1200 - 25

    if y < 25:
        y = 25
    if y > 600 - 25:
        y = 600 - 25

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()