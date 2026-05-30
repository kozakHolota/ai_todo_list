from datetime import date, datetime
from langchain_core.tools import tool
from langgraph.config import get_store

from models.response import Task
from models.state import TaskState

@tool("get_current_date")
def get_current_date() -> str:
    """Return the current date and time in the format YYYY-MM-DD."""
    return datetime.now().isoformat().replace("-", "-")

@tool("add_task")
def add_task(task: Task) -> str:
    """Create a new task. Use when the user wants to add, create, or schedule a new task or reminder."""
    store = get_store()
    store.put(("tasks",), str(task.task_id), task.model_dump(mode="json"))
    return f"Task '{task.name}' created successfully with ID {task.task_id}."

@tool("list_tasks")
def list_tasks():
    """Return all tasks. Use when the user wants to see, show, or get an overview of all their tasks."""
    return list(get_store().search(("tasks",)))


@tool("delete_task")
def delete_task(task_id: str) -> str:
    """Permanently remove a task. Use when the user wants to delete or remove a task entirely — not for marking it done."""
    store = get_store()
    item = store.get(("tasks",), task_id)
    if item is None:
        return f"Task with ID {task_id} not found."
    store.delete(("tasks",), task_id)
    return f"Task {task_id} deleted successfully."


@tool("complete_task")
def complete_task(task_id: str) -> str:
    """Mark an existing task as done. Use when the user says a task is finished, completed, or done. Do not use update_task for this."""
    store = get_store()
    item = store.get(("tasks",), task_id)
    if item is None:
        return f"Task with ID {task_id} not found."
    task_data = item.value
    task_data["state"] = TaskState.COMPLETED
    store.put(("tasks",), task_id, task_data)
    return f"Task '{task_data['name']}' marked as completed."


@tool("get_task_details")
def get_task_details(task_id: str) -> Task:
    """Return full details of one specific task (description, due date, status, etc.). Use instead of list_tasks when the user asks about a particular task by name or id."""
    store = get_store()
    item = store.get(("tasks",), task_id)
    if item is None:
        raise ValueError(f"Task with ID {task_id} not found.")
    return item.value


@tool("update_task")
def update_task(task_id, name: str='', description: str='', due_date: str='', priority: str=''):
    """Edit the title, description, due date, or priority of an existing task. Use for changes to task content — not for marking it complete."""
    store = get_store()
    item = store.get(("tasks",), task_id)
    if item is None:
        raise ValueError(f"Task with ID {task_id} not found.")
    task_data = item.value
    if name:
        task_data["name"] = name
    if due_date:
        task_data["due_date"] = due_date
    if priority:
        task_data["priority"] = priority
    store.put(("tasks",), task_id, task_data)


@tool("search_tasks")
def search_tasks(keyword: str = '', status: str = '', date_range: str = ''):
    """Find tasks by keyword, status, or date range. Use when the user wants to filter or search tasks rather than list all of them. date_range format: 'YYYY-MM-DD:YYYY-MM-DD'."""
    store = get_store()
    tasks = []
    for item in store.search(("tasks",)):
        task = item.value
        if keyword and (keyword.lower() not in task['name'].lower()):
            continue
        if status and task['state'] != status:
            continue
        if date_range:
            due_date_raw = task.get('due_date')
            if not due_date_raw:
                continue
            parts = date_range.split(':')
            if len(parts) != 2:
                continue
            try:
                start_date = date.fromisoformat(parts[0].strip())
                end_date = date.fromisoformat(parts[1].strip())
                task_date = date.fromisoformat(due_date_raw) if isinstance(due_date_raw, str) else due_date_raw
                if not (start_date <= task_date <= end_date):
                    continue
            except ValueError:
                continue
        tasks.append(task)
    return tasks
