import pygame
import sys
import math

pygame.init()

WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (180, 180, 180)

screen.fill(WHITE)

current_color = BLACK
tool = "brush"
drawing = False
start_pos = None
last_pos = None
brush_size = 5
eraser_size = 20

font = pygame.font.SysFont("Verdana", 20)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 50))
    info = f"Tool: {tool} | Colors: 1-Black 2-Red 3-Green 4-Blue 5-Yellow | B-Brush R-Rect C-Circle E-Eraser S-Square T-RightTriangle U-Equilateral H-Rhombus"
    text = font.render(info, True, BLACK)
    screen.blit(text, (10, 12))

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_t:
                tool = "right_triangle"
            elif event.key == pygame.K_u:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_h:
                tool = "rhombus"
            elif event.key == pygame.K_1:
                current_color = BLACK
            elif event.key == pygame.K_2:
                current_color = RED
            elif event.key == pygame.K_3:
                current_color = GREEN
            elif event.key == pygame.K_4:
                current_color = BLUE
            elif event.key == pygame.K_5:
                current_color = YELLOW
            elif event.key == pygame.K_DELETE:
                canvas.fill(WHITE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] > 50:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos and event.pos[1] > 50:
                end_pos = event.pos

                if tool == "rect":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, 2)

                elif tool == "circle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

                elif tool == "square":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    square = pygame.Rect(x1, y1, side, side)
                    pygame.draw.rect(canvas, current_color, square, 2)

                elif tool == "right_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(canvas, current_color, points, 2)

                elif tool == "equilateral_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    side = abs(x2 - x1)
                    height = int((math.sqrt(3)/2) * side)
                    points = [(x1, y1 + height), (x1 + side, y1 + height), (x1 + side//2, y1)]
                    pygame.draw.polygon(canvas, current_color, points, 2)

                elif tool == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                    pygame.draw.polygon(canvas, current_color, points, 2)

            drawing = False
            start_pos = None
            last_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            if event.pos[1] > 50:
                if tool == "brush":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, eraser_size)
                    last_pos = event.pos

    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    draw_ui()
    pygame.display.flip()