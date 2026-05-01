import json
import os

base_dir = os.path.dirname(__file__)
settings_file = os.path.join(base_dir, "settings.json")
leaderboard_file = os.path.join(base_dir, "leaderboard.json")

default_settings = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}

def load_json(path, default_data):
    if not os.path.exists(path):
        save_json(path, default_data)
        return default_data.copy()

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        save_json(path, default_data)
        return default_data.copy()

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_settings():
    settings = load_json(settings_file, default_settings)

    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value

    return settings

def save_settings(settings):
    save_json(settings_file, settings)

def load_leaderboard():
    return load_json(leaderboard_file, [])

def save_score(username, score, distance, coins):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": username,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]

    save_json(leaderboard_file, leaderboard)
