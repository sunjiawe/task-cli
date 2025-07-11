from rich.console import Console
from utils.storage import load_db
from utils.llm_api import get_task_advice

console = Console()

def handle_howto(task_id):
    """Handles the '/howto' command."""
    if not task_id:
        console.print("[red]Task ID is required for /howto command.[/red]")
        return
    db_data = load_db()
    tasks = db_data.get("tasks", [])
    task = next((t for t in tasks if t.get("task_id") == task_id), None)

    if not task:
        console.print(f"[red]Task with ID '{task_id}' not found.[/red]")
        return

    console.print(f"[cyan]Generating advice for task: {task.get('title')}...[/cyan]")
    project_context = db_data
    advice = get_task_advice(task, project_context)
    console.print(f"[bold green]Advice:[/bold green]\n{advice}")

