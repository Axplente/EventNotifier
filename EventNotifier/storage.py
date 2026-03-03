import os
import json


def get_data_path():
    base = os.path.join(os.environ["APPDATA"])
    app_dir = os.path.join(base, "EventNotifier")

    if not os.path.isdir(app_dir):
        os.makedirs(app_dir, exist_ok=True)

    return os.path.join(app_dir, "events.json")


def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        data = {"events": [], "settings": {"run_on_startup": False}}
        save_data(file_path, data)
        return data


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)