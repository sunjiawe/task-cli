import os
import sys
import questionary
from rich.console import Console
from questionary.prompts.autocomplete import WordCompleter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import command handlers
from commands.init import handle_init
from commands.list import handle_list
from commands.decompose import handle_decompose
from commands.howto import handle_howto
from commands.report import handle_report
from commands.qa import handle_qa
from commands.update import handle_update
from commands.help import handle_help
from commands.gantt import handle_gantt

# Import utilities
from utils.storage import query_tasks

console = Console()

# Define subcommands and their descriptions
SUBCOMMANDS = {
    "/list": "List all tasks.",
    "/gantt": "Display a Gantt chart of the project.",
    "/decompose": "Decompose a requirement into new tasks.",
    "/howto": "Get advice on how to perform a specific task.",
    "/report": "Generate a project report.",
    "/qa": "Ask a question about the project.",
    "/update": "Update the status of a task.",
    "/help": "Show this help message.",
    "/exit": "Exit the application.",
}

command_completer = WordCompleter(list(SUBCOMMANDS.keys()), ignore_case=True)

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

            if user_input.lower().strip() == '/exit':
                break

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command == '/list':
                handle_list()
            elif command == '/gantt':
                handle_gantt()
            elif command == '/decompose':
                if not args:
                    args = questionary.text("What is the requirement to decompose?").ask()
                if args:
                    handle_decompose(args)
            elif command == '/howto':
                if not args:
                    args = questionary.text("Enter the task ID for which you need advice:").ask()
                if args:
                    handle_howto(args)
            elif command == '/report':
                handle_report()
            elif command == '/qa':
                if not args:
                    args = questionary.text("What is your question?").ask()
                if args:
                    handle_qa(args)
            elif command == '/update':
                update_parts = user_input.split(maxsplit=2)
                task_id = update_parts[1] if len(update_parts) > 1 else ""
                status = update_parts[2] if len(update_parts) > 2 else ""

                if not task_id:
                    tasks = query_tasks()
                    task_choices = [f"{t['task_id']}: {t['title']}" for t in tasks if t.get('task_id') and t.get('title')]
                    if not task_choices:
                        console.print("[yellow]No tasks to update.[/yellow]")
                        continue
                    selected_task_str = questionary.select("Which task to update?", choices=task_choices).ask()
                    if not selected_task_str:
                        continue
                    task_id = selected_task_str.split(":")[0]

                if not status:
                    status = questionary.select(
                        f"New status for task '{task_id}':",
                        choices=['todo', 'in_progress', 'done', 'blocked'],
                    ).ask()
                
                if task_id and status:
                    handle_update(task_id, status)
            elif command == '/help' or user_input == '/':
                handle_help(SUBCOMMANDS)
            elif command.startswith('/'):
                console.print(f"[yellow]Unknown command: {command}. Type /help for available commands.[/yellow]")
            else:
                # Default action is to decompose the input as a requirement
                handle_decompose(user_input)

        except (KeyboardInterrupt, EOFError):
            break

    console.print("[bold yellow]Goodbye![/bold yellow]")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        handle_init()
    else:
        main_repl()

if __name__ == "__main__":
    main()