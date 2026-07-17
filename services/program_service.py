import json
import os

from services.json_service import load_json_file

PROGRAM_FILE = "static/data/programs.json"

# We point directly to our enrollment database file
ENROLLMENTS_FILE = "static/data/enrollments.json"

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
    return [p for p in get_all_programs() if p["id"] != program_id][:limit]

def save_student_to_db(registration):
    """
    Safely reads, appends a confirmed student to the local JSON file, 
    and writes it back to disk with proper UTF-8 encoding.
    """
    # Ensure file exists and contains a valid list
    if not os.path.exists(ENROLLMENTS_FILE) or os.stat(ENROLLMENTS_FILE).st_size == 0:
        # Added encoding="utf-8" here
        with open(ENROLLMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        # 1. Read existing enrollments (use utf-8)
        with open(ENROLLMENTS_FILE, "r", encoding="utf-8") as f:
            enrollments = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        enrollments = []

    # Check for duplicate entries so we don't double-save on refresh
    if any(e.get("id") == registration["id"] or e.get("paystack_ref") == registration.get("paystack_ref") and e.get("paystack_ref") for e in enrollments):
        return

    # 2. Append new student
    enrollments.append(registration)

    # 3. Write back to disk (added encoding="utf-8" and ensure_ascii=False)
    with open(ENROLLMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(enrollments, f, indent=4, ensure_ascii=False)

        
def find_student_by_id(reg_id):
    """Utility to find a student in the JSON database."""
    if not os.path.exists(ENROLLMENTS_FILE):
        return None
    try:
        with open(ENROLLMENTS_FILE, "r") as f:
            enrollments = json.load(f)
            return next((e for e in enrollments if e.get("id") == reg_id), None)
    except Exception:
        return None
