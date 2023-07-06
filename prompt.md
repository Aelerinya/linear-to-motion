# Linear issue to Motion task

A python script which reads issues from Linear and creates linked tasks in Motion.



The Motion API is authenticated using the X-API-KEY header. It accessed at https://api.usemotion.com/v1/
The api key is in the environment variable `MOTION_API_KEY`

Create three files:

- `model.py`
	- named tuples
		- Issue(title, id, url, estimate, parentId, childrenIds)
		- Cycle(name, startDate, endDate)
		- Task(title, id, url, estimate)
		- Project(title, id, url, tasks)
- `read_linear_issues.py`
	- import Issue, Cycle, Task, Project from `model.py`
	- function `read_issues`
		- read issues from linear API
			- authenticate with  environment variable `LINEAR_API_KEY`
			- endpoint `https://api.linear.app/graphql`
			- graphql query `query ExampleQuery { cycles(first: 1, filter: { isActive: { eq: true } }) { nodes { id name endsAt startsAt issues(filter: { assignee: { email: { eq: "lucie@cryptio.co" } } }) { nodes { assignee { displayName } url title estimate identifier parent { identifier } children { nodes { identifier } } } } } }`
		- call the graphQL endpoint to retrieve the list of issues using the request package
		- return issues as Issue and Cycle
	- function `get_projects`
		- Issues with children are projects
		- If the issue has an estimate different from zero, add an initial task to the project with the same info
		- Return every project
	- function `get_tasks`
	 	- parameters: issues and projects
		- Issues without children are tasks
		- If the issue has a parent, add it to the corresponding project
		- If the issue has no parent, add it to a list of orphan tasks
		- return list of Project and orphan Task
	- function `print_markdown`
		- level 1 heading cycle name
		- print cycle dates
		- level 2 header "Projects"
		- print projects as bullet points
			- print each project task (title, estimate, url)
		- level 2 header "Orphan tasks"
		- print each orphan task (title, estimate, url)
	- if called independently
		- call `read_issues`
		- call `get_projects`
		- call `get_tasks`
		- call `print_markdown`
- `create_motion_projects.py`
	- import Cycle, Task, Project from `model.py`
	- function `get_workspace_id`
		- call /workspaces
			- response example `{ "workspaces": [ { "id": "string", "name": "string" } ] }`
			- on error, print response and exit
		- Find workspace named "Test API"
		- return workspace id
	- function `get_user_id`
		- call /users/me
			- response `{ "id": "string", "name": "string", "email": "string" }`
			- on error, print response and exit
		- return id
	- function `create_task`
		- parameter 1 Task, workspace id, user id, cycle info, optional project id
		- call /tasks
			- example body `{ "dueDate": "2023-06-28T10:11:14.320-06:00", "duration": "NONE", "autoScheduled": { "startDate": "2023-06-28" }, "name": "string", "projectId": "string", "workspaceId": "string", "description": "string", "labels": [ "string" ], "assigneeId": "string" }`
			- example response `{ "id": "string", "name": "string", "description": "string", "workspaceId": "string" }`
			- on error (not code 201), print response and exit
		- dueDate is cycle end date
		- startDate is cycle start date
		- duration field follows estimate value
			- 1: 30
			- 2: 60
			- 3: 120
			- 5: 240
			- 8: 480
		- assignee id is user id
		- name: "[API] " +  task title
		- description: task url
		- label: "API"
	- function `create_project`
		- parameter 1 Project, workspace id, user id, cycle info
		- call /projects
			-body `{ "dueDate": "2023-06-28T10:11:14.306-06:00", "name": "string", "workspaceId": "string", "description": "string", "labels": [ "string" ],  "priority": "MEDIUM" }`
			- on error (not code 201), print response and exit
		- dueDate: cycle end date
		- label: "API"
		- name: "[API] " + project title
		- description: project url
		- for each task, call `create_task`
	- if called independently
		- create example Project variable called "Example task created using the script" with one task
		- create example Cycle from today to next week. dates are iso string
		- call `get_workspace_id`
		- call `get_user_id`
		- call `create_task`
- `main.py`
	- from `read_linear_issues.py`
		- call `read_issues`
		- call `get_projects`
		- call `get_tasks`
	- from `create_motion_projects.py`
		- call `get_workspace_id`
		- call `get_user_id`
		- function `create_project` on every project
		- function `create_task` on every orphan task
