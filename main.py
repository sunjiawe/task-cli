import os
import sys
import questionary
from rich.console import Console
from questionary.prompts.autocomplete import WordCompleter
from utils.storage import init_project, load_db, query_tasks, save_db
from utils.display import display_tasks
from utils.llm_api import decompose_requirement, get_task_advice, generate_report, answer_question

console = Console()

# Define subcommands
SUBCOMMANDS = {
    "/list": "List all tasks.",
    "/decompose": "Decompose a requirement into new tasks.",
    "/howto": "Get advice on how to perform a specific task.",
    "/report": "Generate a project report.",
    "/qa": "Ask a question about the project.",
    "/help": "Show this help message.",
    "/quit": "Exit the application.",
}

command_completer = WordCompleter(list(SUBCOMMANDS.keys()), ignore_case=True)

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

def handle_list():
    """Handles the '/list' command."""
    tasks = query_tasks()
    display_tasks(tasks)

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

def handle_help():
    """Displays the help message."""
    console.print("\n[bold]Available commands:[/bold]")
    for cmd, desc in SUBCOMMANDS.items():
        console.print(f"  [cyan]{cmd}[/cyan]: {desc}")
    console.print("\nType any other text to start decomposing a new requirement.\n")

def main_repl():
    """Main Read-Eval-Print Loop."""
    if not os.path.exists(".xixi/db.json"):
        console.print("[red]Project not initialized. Please run 'init' first.[/red]")
        return

    console.print("[bold green]Welcome to Xixi AI Project Manager![/bold green]")
    console.print("Type a command with a '/' prefix or your requirement to start. Type /help for commands.")

    while True:
        try:
            user_input = questionary.text("> ", completer=command_completer).ask()
            if not user_input:
                continue

            if user_input == "/":
                handle_help()
                continue

            command = user_input.lower().split()[0]

            if command == '/quit':
                break
            elif command == '/list':
                handle_list()
            elif command == '/decompose':
                parts = user_input.split(maxsplit=1)
                requirement = parts[1] if len(parts) > 1 else ""
                if not requirement:
                    requirement = questionary.text("What is the requirement to decompose?").ask()
                if requirement:
                    handle_decompose(requirement)
            elif command == '/howto':
                parts = user_input.split(maxsplit=1)
                task_id = parts[1] if len(parts) > 1 else ""
                if not task_id:
                    task_id = questionary.text("Enter the task ID for which you need advice:").ask()
                if task_id:
                    handle_howto(task_id)
            elif command == '/report':
                handle_report()
            elif command == '/qa':
                parts = user_input.split(maxsplit=1)
                question = parts[1] if len(parts) > 1 else ""
                if not question:
                    question = questionary.text("What is your question?").ask()
                if question:
                    handle_qa(question)
            elif command == '/help':
                handle_help()
            elif user_input.startswith('/'):
                console.print(f"[yellow]Unknown command: {user_input}. Type /help for available commands.[/yellow]")
            else:
                handle_decompose(user_input)
        except KeyboardInterrupt:
            break

    console.print("[bold yellow]Goodbye![/bold yellow]")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        handle_init()
    else:
        main_repl()