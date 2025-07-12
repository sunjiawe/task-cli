import os
import questionary
from rich.console import Console
from ..utils.storage import init_project

console = Console()

def handle_init():
    """Handles the 'init' command."""
    if os.path.exists(".xixi/db.json"):
        console.print("[yellow]Project already initialized.[/yellow]")
        return

    project_name = questionary.text("Enter project name:").ask()
    project_goal = questionary.text("Enter project goal:").ask()

    if not project_name or not project_goal:
        console.print("[red]Project name and goal cannot be empty.[/red]")
        return

    init_project(project_name, project_goal)
    console.print("[green]Project initialized successfully![/green]")
