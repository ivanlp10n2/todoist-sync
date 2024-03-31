from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Project:
    id: int
    name: str

@dataclass
class Category:
    id: int
    name: str

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    labels: List[str] = None
    comments: List[str] = None
    finalized_date: str = ""
    created_date: str = ""
    priority: int = 0

class TodoistAPI(ABC):
    @abstractmethod
    def get_projects(self) -> List[Project]:
        pass

    @abstractmethod
    def get_project_categories(self, project_id: int) -> List[Category]:
        pass

    @abstractmethod
    def get_tasks(self, category_id: int) -> List[Task]:
        pass

    @abstractmethod
    def create_project(self, name: str) -> Project:
        pass

    @abstractmethod
    def create_category(self, project_id: int, name: str) -> Category:
        pass

    @abstractmethod
    def move_task(self, task_id: int, category_id: int) -> None:
        pass

    @abstractmethod
    def copy_task(self, task_id: int, category_id: int) -> None:
        pass

class TodoistAPIImpl(TodoistAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_projects(self) -> List[Project]:
        # Implementation to retrieve projects from Todoist API
        pass

    def get_project_categories(self, project_id: int) -> List[Category]:
        # Implementation to retrieve project categories from Todoist API
        pass

    def get_tasks(self, category_id: int) -> List[Task]:
        # Implementation to retrieve tasks from Todoist API
        pass

    def create_project(self, name: str) -> Project:
        # Implementation to create a new project using Todoist API
        pass

    def create_category(self, project_id: int, name: str) -> Category:
        # Implementation to create a new category using Todoist API
        pass

    def move_task(self, task_id: int, category_id: int) -> None:
        # Implementation to move a task to a different category using Todoist API
        pass

    def copy_task(self, task_id: int, category_id: int) -> None:
        # Implementation to copy a task to a different category using Todoist API
        pass
