from rich.console import Console
from ..utils.storage import load_db, save_db
from ..utils.display import display_tasks
from ..utils.llm_api import decompose_requirement

console = Console()

def handle_decompose(requirement):
    """Handles the '/decompose' command with a multi-turn conversation for refinement."""
    console.print(f"[cyan]Decomposing requirement: {requirement}...[/cyan]")
    db_data = load_db()
    project_context = db_data
    
    # Initial decomposition
    new_tasks = decompose_requirement(requirement, project_context)

    if not new_tasks:
        console.print("[yellow]No new tasks were generated.[/yellow]")
        return

    while True:
        console.print("[green]Generated tasks:[/green]")
        display_tasks(new_tasks)
        
        console.print("\n[bold]Are these tasks correct? (yes/no/feedback)[/bold]")
        user_input = console.input("> ").lower().strip()

        if user_input == 'yes':
            db_data["tasks"].extend(new_tasks)
            save_db(db_data)
            console.print("[green]Tasks added to the project.[/green]")
            break
        elif user_input == 'no':
            console.print("[yellow]Tasks discarded.[/yellow]")
            break
        else:
            # Treat any other input as feedback for refinement
            feedback = user_input
            console.print(f"[cyan]Revising tasks based on feedback: {feedback}...[/cyan]")
            # Pass the feedback to the LLM API
            new_tasks = decompose_requirement(requirement, project_context, feedback=feedback, previous_tasks=new_tasks)
            if not new_tasks:
                console.print("[yellow]Failed to generate new tasks based on feedback.[/yellow]")
                break
