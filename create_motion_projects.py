import requests
import os
from datetime import datetime
import config

from model import Cycle, Task, Project

def get_headers():
    return {
        "X-API-KEY": config.motion_api_key
    }

def get_workspace_id():
    response = requests.get("https://api.usemotion.com/v1/workspaces", headers=get_headers())
    if response.status_code != 200:
        print(response.text)
        exit()
    workspaces = response.json()["workspaces"]
    for workspace in workspaces:
        if workspace["name"] == config.workspace_name:
            return workspace["id"]
    print("Workspace 'Test API' not found")
    exit()

def get_user_id():
    response = requests.get("https://api.usemotion.com/v1/users/me", headers=get_headers())
    if response.status_code != 200:
        print(response.text)
        exit()
    return response.json()["id"]

def create_task(task: Task, workspace_id: str, user_id: str, cycle_info: Cycle, project_id: str|None =None):
    due_date = cycle_info.endDate
    start_date = cycle_info.startDate
    duration = {
        1: 30,
        2: 60,
        3: 120,
        5: 240,
        8: 480
    }.get(task.estimate, 0)
    name = f"[API] {task.title}"
    description = task.url
    labels = ["API"]
    assignee_id = user_id

    body = {
        "dueDate": due_date,
        "duration": duration,
        "autoScheduled": {
            "startDate": start_date
        },
        "name": name,
        "workspaceId": workspace_id,
        "description": description,
        "labels": labels,
        "assigneeId": assignee_id
    }

    if project_id:
        body["projectId"] = project_id

    response = requests.post("https://api.usemotion.com/v1/tasks", headers=get_headers(), json=body)
    if response.status_code != 201:
        print(response.text)
        exit()

def create_project(project: Project, workspace_id: str, user_id: str, cycle_info: Cycle):
    due_date = cycle_info.endDate
    name = f"[API] {project.title}"
    description = project.url
    labels = ["API"]
    priority = "MEDIUM"

    body = {
        "dueDate": due_date,
        "name": name,
        "workspaceId": workspace_id,
        "description": description,
        "labels": labels,
        "priority": priority
    }

    response = requests.post("https://api.usemotion.com/v1/projects", headers=get_headers(), json=body)
    if response.status_code != 201:
        print(response.text)
        exit()

    project_id = response.json()["id"]
    for task in project.tasks:
        create_task(task, workspace_id, user_id, cycle_info, project_id)

if __name__ == "__main__":
    example_project = Project(
        title="Example task created using the script",
        id="project_id",
        url="https://example.com/project",
        tasks=[
            Task(
                title="Example task",
                id="task_id",
                url="https://example.com/task",
                estimate=3
            )
        ]
    )

    example_cycle = Cycle(
        name="Example Cycle",
        startDate=datetime.now().isoformat(),
        endDate=(datetime.now().isoformat())
    )

    workspace_id = get_workspace_id()
    user_id = get_user_id()

    create_task(example_project.tasks[0], workspace_id, user_id, example_cycle)
    create_project(example_project, workspace_id, user_id, example_cycle)