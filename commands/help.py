from rich.console import Console

console = Console()

def handle_help(subcommands):
    """Displays the help message."""
    console.print("\n[bold]Available commands:[/bold]")
    for cmd, desc in subcommands.items():
        console.print(f"  [cyan]{cmd}[/cyan]: {desc}")
    console.print("\nType any other text to start decomposing a new requirement.\n")

