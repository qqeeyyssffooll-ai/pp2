import pygame
from racer import width, height, fps, RacerGame
from ui import Button, draw_text, username_screen, white, dark, yellow, green, red
from persistence import load_settings, save_settings, load_leaderboard, save_score

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)
small_font = pygame.font.SysFont("Verdana", 16)

settings = load_settings()
username = "Player"
last_result = None

def main_menu():
    global username

    buttons = [
        Button(100, 190, 200, 45, "Play", font),
        Button(100, 250, 200, 45, "Leaderboard", font),
        Button(100, 310, 200, 45, "Settings", font),
        Button(100, 370, 200, 45, "Quit", font)
    ]

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if buttons[0].clicked(event):
                username = username_screen(screen, clock, width, height)
                return "play"
            if buttons[1].clicked(event):
                return "leaderboard"
            if buttons[2].clicked(event):
                return "settings"
            if buttons[3].clicked(event):
                pygame.quit()
                raise SystemExit

        screen.fill(dark)
        draw_text(screen, "TSIS3 RACER", 36, white, width // 2, 100)
        draw_text(screen, "Advanced Driving Game", 17, yellow, width // 2, 140)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

def leaderboard_screen():
    back = Button(110, 530, 180, 42, "Back", font)

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if back.clicked(event):
                return "menu"

        screen.fill(dark)
        draw_text(screen, "Leaderboard Top 10", 28, white, width // 2, 60)

        data = load_leaderboard()
        if not data:
            draw_text(screen, "No scores yet", 20, yellow, width // 2, 180)
        else:
            y = 115
            draw_text(screen, "Rank   Name       Score    Distance", 14, yellow, 35, 90, center=False)
            for i, row in enumerate(data, start=1):
                text = f"{i:<5} {row['name'][:8]:<9} {row['score']:<7} {row['distance']}m"
                surface = small_font.render(text, True, white)
                screen.blit(surface, (35, y))
                y += 34

        back.draw(screen)
        pygame.display.flip()

def settings_screen():
    global settings

    sound = Button(70, 160, 260, 42, "", font)
    color = Button(70, 230, 260, 42, "", font)
    difficulty = Button(70, 300, 260, 42, "", font)
    back = Button(110, 430, 180, 42, "Back", font)

    colors = ["blue", "red", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        clock.tick(fps)

        sound.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color.text = f"Car color: {settings['car_color']}"
        difficulty.text = f"Difficulty: {settings['difficulty']}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if sound.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color.clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            if difficulty.clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            if back.clicked(event):
                return "menu"

        screen.fill(dark)
        draw_text(screen, "Settings", 32, white, width // 2, 80)
        sound.draw(screen)
        color.draw(screen)
        difficulty.draw(screen)
        back.draw(screen)
        pygame.display.flip()

def game_over_screen(result, finished=False):
    retry = Button(95, 365, 210, 42, "Retry", font)
    menu = Button(95, 425, 210, 42, "Main Menu", font)

    title = "FINISHED!" if finished else "GAME OVER"
    color = green if finished else red

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if retry.clicked(event):
                return "play"
            if menu.clicked(event):
                return "menu"

        screen.fill(dark)
        draw_text(screen, title, 36, color, width // 2, 105)
        draw_text(screen, f"Player: {username}", 20, white, width // 2, 175)
        draw_text(screen, f"Score: {result['score']}", 20, white, width // 2, 215)
        draw_text(screen, f"Distance: {result['distance']}m", 20, white, width // 2, 250)
        draw_text(screen, f"Coins: {result['coins']}", 20, white, width // 2, 285)
        retry.draw(screen)
        menu.draw(screen)
        pygame.display.flip()

def play_game():
    game = RacerGame(screen, clock, username, settings)
    status = game.run()

    result = {
        "score": game.score,
        "distance": int(game.distance),
        "coins": game.coins
    }

    save_score(username, game.score, game.distance, game.coins)

    return game_over_screen(result, finished=(status == "finished"))

def main():
    state = "menu"

    while True:
        if state == "menu":
            state = main_menu()
        elif state == "play":
            state = play_game()
        elif state == "leaderboard":
            state = leaderboard_screen()
        elif state == "settings":
            state = settings_screen()


if __name__ == "__main__":
    main()