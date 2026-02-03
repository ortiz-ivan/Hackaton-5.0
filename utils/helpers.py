import json
import os

def load_obstacle_data():
    # Buscamos el archivo que acabas de crear
    path = os.path.join("data", "obstacles.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró data/obstacles.json")
        return {}
    