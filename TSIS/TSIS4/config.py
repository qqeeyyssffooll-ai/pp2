import os

width = 800
height = 600
cell_size = 20
fps = 60

top_panel = 60
cols = width // cell_size
rows = (height - top_panel) // cell_size

base_speed = 8
level_up_every = 5
obstacles_per_level = 4

image_dir = os.path.join(os.path.dirname(__file__), "images")
settings_file = os.path.join(os.path.dirname(__file__), "settings.json")

image_files = {
    "food": "food.png",
    "poison": "poison.png",
    "speed": "speed.png",
    "slow": "slow.png",
    "shield": "shield.png",
    "snake_head": "snake_head.png",
    "snake_body": "snake_body.png",
    "obstacle": "obstacle.png",
    "background": "background.png"
}

db_config = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "q3e1t7u5",
    "port": 5432,
}
