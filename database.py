
import json
import os
from datetime import datetime

# JSON-Datei Pfad
db_path = "user_data.json"

# Laden der Datenbank
def load_db():
    if os.path.exists(db_path):
        with open(db_path, "r") as file:
            return json.load(file)
    return {}

# Speichern der Datenbank
def save_db(data):
    with open(db_path, "w") as file:
        json.dump(data, file, indent=4)

# Benutzerdaten speichern
def save_user_data(user_id, user_data):
    data = load_db()
    if user_id not in data:
        data[user_id] = []
    user_data["timestamp"] = datetime.now().isoformat()
    data[user_id].append(user_data)
    save_db(data)

# Benutzerdaten abrufen
def get_user_history(user_id):
    data = load_db()
    return data.get(user_id, [])