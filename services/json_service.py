import os
import json
from flask import current_app

def load_json_file(filename):
    """Safely load JSON files."""
    file_path = os.path.join(current_app.root_path, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found!")
        return {}