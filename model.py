from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()

Issue = namedtuple('Issue', ['title', 'id', 'url', 'estimate', 'parentId', 'childrenIds'])
Cycle = namedtuple('Cycle', ['name', 'startDate', 'endDate'])
Task = namedtuple('Task', ['title', 'id', 'url', 'estimate'])
Project = namedtuple('Project', ['title', 'id', 'url', 'tasks'])