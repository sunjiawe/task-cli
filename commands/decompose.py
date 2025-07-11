from rich.console import Console
from utils.storage import load_db, save_db
from utils.display import display_tasks
from utils.llm_api import decompose_requirement

console = Console()

def handle_decompose(requirement):
    """Handles the '/decompose' command."""
    console.print(f"[cyan]Decomposing requirement: {requirement}...[/cyan]")
    db_data = load_db()
    project_context = db_data
    new_tasks = decompose_requirement(requirement, project_context)
    if new_tasks:
        db_data["tasks"].extend(new_tasks)
        save_db(db_data)
        console.print("[green]New tasks added:[/green]")
        display_tasks(new_tasks)
    else:
        console.print("[yellow]No new tasks were generated.[/yellow]")
