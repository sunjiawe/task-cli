import json
import os
import uuid
from datetime import datetime

# Define constants for directories and files
DB_DIR = ".xixi"
DB_FILE = os.path.join(DB_DIR, "db.json")
CONFIG_FILE = os.path.join(DB_DIR, "config.json")

def init_project(name, goal):
    """
    Initializes the project database and config file.
    """
    os.makedirs(DB_DIR, exist_ok=True)

    # Initialize database
    project_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    db_data = {
        "project": {
            "project_id": project_id,
            "project_name": name,
            "project_goal": goal,
            "created_at": created_at,
        },
        "tasks": [],
    }
    save_db(db_data)

    # Initialize config
    if not os.path.exists(CONFIG_FILE):
        config_data = {"language": "en"}
        save_config(config_data)

    return db_data

def load_db():
    """
    Loads the entire JSON database.
    """
    if not os.path.exists(DB_FILE):
        return None
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_db(data):
    """
    Saves the entire data object back to the JSON file.
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_config():
    """
    Loads the config file.
    """
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_config(data):
    """
    Saves the config data back to the JSON file.
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def query_tasks(status=None, overdue=None):
    """
    Queries tasks based on criteria.
    """
    data = load_db()
    if not data:
        return []
    
    tasks = data.get("tasks", [])
    
    if status:
        tasks = [t for t in tasks if t.get("status") in status]
        
    if overdue:
        today = datetime.now().date()
        tasks = [t for t in tasks if t.get("due_date") and datetime.fromisoformat(t["due_date"]).date() < today]
        
    return tasks