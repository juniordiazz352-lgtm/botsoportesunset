import json
import os

DB_FILE = "data.json"

def load():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_form(user_id, responses):
    data = load()
    data[str(user_id)] = responses
    save(data)
