import pygame

playlist = ["queen", "yesterday", "rickroll"]
current = 0
paused = False
duration = 0

def load_track():
    global duration

    pygame.mixer.music.load(f"music/{playlist[current]}.mp3")
    track = pygame.mixer.Sound(f"music/{playlist[current]}.mp3")
    duration = track.get_length()

def play():
    global paused
    pygame.mixer.music.play()
    paused = False

def pause():
    global paused
    if not paused:
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False

def next_track():
    global current
    current += 1
    if current >= len(playlist):
        current = 0
    load_track()
    pygame.mixer.music.play()

def prev_track():
    global current
    current -= 1
    if current < 0:
        current = len(playlist) - 1
    load_track()
    pygame.mixer.music.play()

def get_name():
    return playlist[current]

def get_progress():
    current_time = pygame.mixer.music.get_pos() / 1000
    progress = current_time / duration if duration > 0 else 0
    return progress