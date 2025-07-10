import json
import os
import uuid
from datetime import datetime

DB_FILE = ".xixi/db.json"

def init_project(name, goal):
    """
    Initializes the project database file.
    """
    os.makedirs(".xixi", exist_ok=True)
    project_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    data = {
        "project": {
            "project_id": project_id,
            "project_name": name,
            "project_goal": goal,
            "created_at": created_at,
        },
        "tasks": [],
    }
    save_db(data)
    return data

def load_db():
    """
    Loads the entire JSON database.
    """
    if not os.path.exists(DB_FILE):
        return None
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    """
    Saves the entire data object back to the JSON file.
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
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
