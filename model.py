from typing import NamedTuple

class Issue(NamedTuple):
    title: str
    id: str
    url: str
    estimate: int
    parentId: str | None
    childrenIds: list[str]

class Cycle(NamedTuple):
    name: str
    startDate: str
    endDate: str

class Task(NamedTuple):
    title: str
    id: str
    url: str
    estimate: int

class Project(NamedTuple):
    title: str
    id: str
    url: str
    tasks: list[Task]