from rich.console import Console
from utils.storage import load_db, query_tasks
from utils.llm_api import answer_question

console = Console()

def handle_qa(question):
    """Handles the '/qa' command."""
    console.print(f"[cyan]Answering question: {question}...[/cyan]")
    db_data = load_db()
    project_context = {
        "project": db_data.get("project"),
        "tasks": query_tasks(status=['todo', 'in_progress', 'blocked']) # Default context
    }
    answer = answer_question(question, project_context)
    console.print(f"[bold green]Answer:[/bold green]\n{answer}")

