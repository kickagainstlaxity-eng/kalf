from services.json_service import load_json_file

PROGRAM_FILE = "static/data/programs.json"


def load_programs():
    """Load all programs from the JSON file."""
    return load_json_file(PROGRAM_FILE)


def get_all_programs():
    """Return a flattened list of all programs."""
    data = load_programs()

    programs = []

    for category, items in data.items():
        for item in items:
            item["category"] = category
            programs.append(item)

    return programs


def find_program_by_id(prog_id):
    """Find a program and its category."""
    data = load_programs()

    if not data:
        return None, None

    for category, items in data.items():
        for item in items:
            if item.get("id") == prog_id:
                return item, category.lower()

    return None, None


def get_recommended(program_id, limit=3):
    """Return recommended programs excluding the current one."""
    return [
        p for p in get_all_programs()
        if p["id"] != program_id
    ][:limit]