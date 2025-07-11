from rich.console import Console
from utils.storage import load_db, save_db

console = Console()

def handle_update(task_id, status):
    """Handles the '/update' command."""
    if not task_id or not status:
        console.print("[red]Task ID and status are required for /update command.[/red]")
        return

    db_data = load_db()
    tasks = db_data.get("tasks", [])
    task = next((t for t in tasks if t.get("task_id") == task_id), None)

    if not task:
        console.print(f"[red]Task with ID '{task_id}' not found.[/red]")
        return

    if status not in ['todo', 'in_progress', 'done', 'blocked']:
        console.print(f"[red]Invalid status: {status}. Choose from 'todo', 'in_progress', 'done', 'blocked'.[/red]")
        return

    task['status'] = status
    save_db(db_data)
    console.print(f"[green]Task '{task_id}' status updated to '{status}'.[/green]")
