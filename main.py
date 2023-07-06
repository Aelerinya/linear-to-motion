import sys
from read_linear_issues import read_issues, get_projects, get_tasks
from create_motion_projects import get_workspace_id, get_user_id, create_project, create_task

def main():
    # Read issues from Linear
    issues, cycle = read_issues()
    
    # Get projects and tasks
    projects = get_projects(issues)
    orphan_tasks = get_tasks(issues, projects)
    
    # Get workspace and user IDs
    workspace_id = get_workspace_id()
    user_id = get_user_id()
    
    # Create projects in Motion
    for project in projects:
        create_project(project, workspace_id, user_id, cycle)
    
    # Create orphan tasks in Motion
    for task in orphan_tasks:
        create_task(task, workspace_id, user_id, cycle)

if __name__ == "__main__":
    main()