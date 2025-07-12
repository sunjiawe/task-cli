from rich.console import Console
from ..utils.storage import load_db
from ..utils.llm_api import generate_report

console = Console()

def handle_report():
    """Handles the '/report' command."""
    console.print("[cyan]Generating project report...[/cyan]")
    db_data = load_db()
    project_context = {
        "project": db_data.get("project"),
        "tasks": db_data.get("tasks", [])
    }
    report = generate_report(project_context)
    console.print(f"[bold green]Project Report:[/bold green]\n{report}")

