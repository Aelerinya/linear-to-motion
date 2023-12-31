import os
import requests
from model import Issue, Cycle, Task, Project
from string import Template
import config

def read_issues():
    query = Template("""
    query ExampleQuery {
        cycles(first: 1, filter: { isNext: { eq: true } }) {
            nodes {
                id
                name
                endsAt
                startsAt
                issues(filter: { assignee: { email: { eq: "$email" } } }) {
                    nodes {
                        assignee {
                            displayName
                        }
                        url
                        title
                        estimate
                        identifier
                        parent {
                            identifier
                        }
                        children {
                            nodes {
                                identifier
                            }
                        }
                    }
                }
            }
        }
    }
    """).substitute(email=config.linear_email)

    headers = {
        "Authorization": f"Bearer {config.linear_api_key}",
    }

    response = requests.post("https://api.linear.app/graphql", json={"query": query}, headers=headers)
    data = response.json()

    cycles = data["data"]["cycles"]["nodes"]
    issues = cycles[0]["issues"]["nodes"]

    issue_list: list[Issue] = []
    for issue in issues:
        url = issue["url"]
        title = issue["title"]
        estimate = issue["estimate"]
        identifier = issue["identifier"]
        parent = issue["parent"]["identifier"] if issue["parent"] else None
        children = [child["identifier"] for child in issue["children"]["nodes"]]
        issue_list.append(Issue(title, identifier, url, estimate, parent, children))

    cycle = Cycle(cycles[0]["name"], cycles[0]["startsAt"], cycles[0]["endsAt"])

    return issue_list, cycle

def get_projects(issues: list[Issue]):
    projects: list[Project] = []
    for issue in issues:
        if issue.childrenIds:
            tasks: list[Task] = []
            if issue.estimate != 0:
                task = Task(issue.title, issue.id, issue.url, issue.estimate)
                tasks.append(task)
            project = Project(issue.title, issue.id, issue.url, tasks)
            projects.append(project)
    return projects

def get_tasks(issues: list[Issue], projects: list[Project]):
    tasks: list[Task] = []
    for issue in issues:
        if not issue.childrenIds:
            if issue.parentId:
                for project in projects:
                    if project.id == issue.parentId:
                        task = Task(issue.title, issue.id, issue.url, issue.estimate)
                        project.tasks.append(task)
            else:
                task = Task(issue.title, issue.id, issue.url, issue.estimate)
                tasks.append(task)
    return tasks

def print_markdown(cycle: Cycle, projects: list[Project], tasks: list[Task]):
    print(f"# {cycle.name}")
    print(f"Start Date: {cycle.startDate}")
    print(f"End Date: {cycle.endDate}")
    print("\n## Projects")
    for project in projects:
        print(f"- {project.title}")
        for task in project.tasks:
            print(f"  - {task.title} (Estimate: {task.estimate}, URL: {task.url})")
    print("\n## Orphan tasks")
    for task in tasks:
        print(f"- {task.title} (Estimate: {task.estimate}, URL: {task.url})")

if __name__ == "__main__":
    issues, cycle = read_issues()
    projects = get_projects(issues)
    tasks = get_tasks(issues, projects)
    print_markdown(cycle, projects, tasks)