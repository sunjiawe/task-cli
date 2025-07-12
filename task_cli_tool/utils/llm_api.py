import json
import yaml
from datetime import datetime
from .call_llm import call_llm
from .storage import get_config

def decompose_requirement(requirement: str, project_context: dict, feedback: str = None, previous_tasks: list = None) -> list:
    """
    Decomposes a user's requirement into a list of tasks, with optional feedback loops.
    """
    config = get_config()
    language = config.get("language", "en")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    feedback_prompt = ""
    if feedback and previous_tasks:
        feedback_prompt = f"""## Previous Attempt
Here was the previous list of tasks you generated:
{json.dumps(previous_tasks, indent=2)}

The user has provided the following feedback for refinement:
User Feedback: "{feedback}"

Please revise the task list based on this feedback."""

    prompt = f"""
# Role: AI Project Manager

## Context
- Current Date: {current_date}
- Language: {language}
- Project Name: {project_context['project']['project_name']}
- Project Goal: {project_context['project']['project_goal']}
- Existing Tasks: {json.dumps(project_context['tasks'], indent=2)}

## Request
Decompose the following user requirement into a list of actionable tasks.

Requirement: "{requirement}"

{feedback_prompt}

## Rules
- Output must be a valid YAML list of task objects.
- Each task must have `task_id`, `title`, `status` ('todo'), and `created_at`.
- Infer `description`, `difficulty` (1-5), `estimated_hours`, `due_date`, and `dependencies` where possible.
- `parent_id` should be used for sub-tasks.
- Ensure `task_id` is a short, unique, and descriptive string (e.g., 'setup-db', 'create-api-endpoints').
- Do not include tasks that already exist.
- If the requirement is simple, create a single task.
- If the requirement is a question or cannot be decomposed, return an empty list.

## Output Format
```yaml
- task_id: "example-task-1"
  parent_id: null
  title: "Example Task 1"
  description: "An example task."
  status: "todo"
  difficulty: 2
  estimated_hours: 4
  due_date: "YYYY-MM-DD"
  dependencies: []
  created_at: "iso-timestamp"
  updated_at: "iso-timestamp"
```
"""
    response = call_llm(prompt)
    try:
        # Extract YAML from the response
        yaml_str = response.strip().split('```yaml')[1].split('```')[0]
        tasks = yaml.safe_load(yaml_str)
        # Basic validation
        if isinstance(tasks, list):
            return tasks
        return []
    except (yaml.YAMLError, IndexError):
        return []

def get_task_advice(task: dict, project_context: dict) -> str:
    """
    Generates advice on how to approach a specific task.
    """
    config = get_config()
    language = config.get("language", "en")
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
# Role: AI Tech Lead

## Context
- Current Date: {current_date}
- Language: {language}
- Project Name: {project_context['project']['project_name']}
- Project Goal: {project_context['project']['project_goal']}
- Task to Advise On: {json.dumps(task, indent=2)}

## Request
Provide clear, actionable advice and concrete steps on how to complete the given task.
Focus on best practices and potential pitfalls.

## Output Format
Provide the advice as a concise, well-formatted markdown string.
"""
    return call_llm(prompt)

def generate_report(project_context: dict) -> str:
    """
    Generates a project status report.
    """
    config = get_config()
    language = config.get("language", "en")
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
# Role: AI Project Manager

## Context
- Current Date: {current_date}
- Language: {language}
- Project Data: {json.dumps(project_context, indent=2)}

## Request
Generate a comprehensive project status report in Markdown format. The report should include:
1.  **Project Summary**: A brief overview of the project name, goal, and overall progress.
2.  **Task Status Breakdown**: A summary of tasks by status (Done, In Progress, To Do, Blocked).
3.  **Key Accomplishments**: Highlight recently completed tasks.
4.  **Upcoming Priorities**: List the next critical tasks.
5.  **Risks and Blockers**: Identify any tasks that are blocked or overdue.

## Output Format
A single, well-formatted Markdown string.
"""
    return call_llm(prompt)

def answer_question(question: str, project_context: dict) -> str:
    """
    Answers a user's question based on the project context.
    """
    config = get_config()
    language = config.get("language", "en")
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
# Role: AI Project Assistant

## Context
- Current Date: {current_date}
- Language: {language}
- Project Data: {json.dumps(project_context, indent=2)}

## Question
"{question}"

## Request
Based *only* on the provided project data, answer the user's question.
If the answer cannot be found in the context, state that clearly.

## Output Format
A concise and direct answer.
"""
    return call_llm(prompt)