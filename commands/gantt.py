import os
import json
from rich.console import Console
from datetime import datetime, timedelta
from utils.storage import query_tasks, load_db

console = Console()

def handle_gantt():
    """Handles the '/gantt' command by generating a native HTML Gantt chart."""
    tasks = query_tasks()
    db_data = load_db()
    project_name = db_data.get("project", {}).get("project_name", "Project")

    if not tasks:
        console.print("[yellow]No tasks found to generate a Gantt chart.[/yellow]")
        return

    tasks_with_dates = []
    for task in tasks:
        start_date_str = task.get("created_at")
        due_date_str = task.get("due_date")

        if start_date_str and due_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00")).date()
                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00")).date()
                if due_date < start_date:
                    due_date = start_date

                duration = due_date - start_date
                # Pass more task details for the tooltip
                tasks_with_dates.append({
                    "id": task.get("task_id"),
                    "title": task.get("title"),
                    "description": task.get("description", "No description."),
                    "start": start_date,
                    "end": due_date,
                    "duration": duration,
                    "status": task.get("status", "todo"),
                    "difficulty": task.get("difficulty", "N/A"),
                    "estimated_hours": task.get("estimated_hours", "N/A"),
                    "dependencies": task.get("dependencies", [])
                })
            except (ValueError, TypeError):
                continue

    if not tasks_with_dates:
        console.print("[yellow]No tasks with valid start and due dates found.[/yellow]")
        return

    tasks_map = {t["id"]: t for t in tasks_with_dates}

    # Iteratively adjust start dates for dependencies
    for _ in range(len(tasks_with_dates) + 1):
        changed = False
        for task in tasks_with_dates:
            max_dep_end_date = None
            for dep_id in task["dependencies"]:
                dep_task = tasks_map.get(dep_id)
                if dep_task:
                    if max_dep_end_date is None or dep_task["end"] > max_dep_end_date:
                        max_dep_end_date = dep_task["end"]
            
            if max_dep_end_date and task["start"] < max_dep_end_date:
                task["start"] = max_dep_end_date
                # task["end"] = task["start"] + task["duration"]  # 暂时不推移deadline，否则项目周期会被拉得很长
                changed = True

        if not changed:
            break
    
    min_date = min(t["start"] for t in tasks_with_dates)
    max_date = max(t["end"] for t in tasks_with_dates)

    # Convert date objects back to strings for JSON and remove temp fields
    for task in tasks_with_dates:
        task["start"] = task["start"].isoformat()
        task["end"] = task["end"].isoformat()
        if "duration" in task:
            del task["duration"]

    # Load the template
    try:
        with open("templates/gantt_template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        console.print("[red]Error: Gantt chart template not found.[/red]")
        return

    # Inject data into the template
    rendered_html = template.replace("{{ project_name }}", project_name)
    rendered_html = rendered_html.replace("{{ tasks_json }}", json.dumps(tasks_with_dates))
    rendered_html = rendered_html.replace("{{ min_date }}", min_date.isoformat())
    rendered_html = rendered_html.replace("{{ max_date }}", max_date.isoformat())

    # Save the rendered HTML
    output_path = "gantt.html"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        console.print(f"[green]Successfully generated Gantt chart: [bold link=file://{os.path.abspath(output_path)}]{output_path}[/bold link][/green]")
    except IOError as e:
        console.print(f"[red]Error writing to file {output_path}: {e}[/red]")
