from ..utils.storage import query_tasks
from ..utils.display import display_tasks

def handle_list():
    """Handles the '/list' command."""
    tasks = query_tasks()
    display_tasks(tasks)