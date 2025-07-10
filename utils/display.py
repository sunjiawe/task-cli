from rich.table import Table
from rich.console import Console

console = Console()

def display_tasks(tasks):
    """Displays tasks in a formatted table."""
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Due Date", style="yellow")

    for task in tasks:
        table.add_row(
            task.get("task_id", "N/A"),
            task.get("title", "N/A"),
            task.get("status", "N/A"),
            task.get("due_date", "N/A"),
        )

    console.print(table)
