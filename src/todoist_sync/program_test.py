import pytest
from todoist_sync.todoist_api import TodoistAPI, Project, Category, Task
from todoist_sync.program import sync_new_month
from typing import List, Dict
from todoist_sync.program import sync_new_month
from todoist_sync.todoist_api import TodoistAPI, Project, Category, Task

class MockTodoistAPI(TodoistAPI):
    def __init__(self):
        self.projects = []
        self.categories = {}
        self.tasks = {}
        self.project_id_counter = 1
        self.category_id_counter = 1
        self.task_id_counter = 1

    def get_projects(self) -> List[Project]:
        return self.projects

    def get_project_categories(self, project_id: int) -> List[Category]:
        return self.categories.get(project_id, [])

    def get_tasks(self, category_id: int) -> List[Task]:
        return self.tasks.get(category_id, [])

    def create_project(self, name: str) -> Project:
        project = Project(id=self.project_id_counter, name=name)
        self.project_id_counter += 1
        self.projects.append(project)
        return project

    def create_category(self, project_id: int, name: str) -> Category:
        category = Category(id=self.category_id_counter, name=name)
        self.category_id_counter += 1
        self.categories.setdefault(project_id, []).append(category)
        return category

    def move_task(self, task_id: int, category_id: int) -> None:
        for project_id, tasks in self.tasks.items():
            task = next((t for t in tasks if t.id == task_id), None)
            if task:
                self.tasks[project_id] = [t for t in tasks if t.id != task_id]
                self.tasks.setdefault(category_id, []).append(task)
                break

    def copy_task(self, task_id: int, category_id: int) -> None:
        for project_id, tasks in self.tasks.items():
            task = next((t for t in tasks if t.id == task_id), None)
            if task:
                new_task = Task(
                    id=self.task_id_counter,
                    title=task.title,
                    description=task.description,
                    labels=task.labels,
                    comments=task.comments,
                    finalized_date=task.finalized_date,
                    created_date=task.created_date,
                    priority=task.priority
                )
                self.task_id_counter += 1
                self.tasks.setdefault(category_id, []).append(new_task)
                break


def test_sync_new_month():
    # Create an instance of the mock TodoistAPI
    todoist_api = MockTodoistAPI()

    # Create sample projects
    project1 = todoist_api.create_project("Old Project")
    project2 = todoist_api.create_project("New Project")

    # Create sample categories for the old project
    category1 = todoist_api.create_category(project1.id, "Category 1")
    category2 = todoist_api.create_category(project1.id, "Category 2")
    category3 = todoist_api.create_category(project1.id, "Category 3_task")

    # Create sample tasks for the old project
    task1 = Task(id=1, title="Task 1", description="Description 1")
    task2 = Task(id=2, title="Task 2", description="Description 2")
    task3 = Task(id=3, title="Task 3", description="Description 3")
    task4 = Task(id=4, title="Task 4", description="Description 4")
    task5 = Task(id=5, title="Task 5", description="Description 5")

    todoist_api.tasks[category1.id] = [task1, task2]
    todoist_api.tasks[category2.id] = [task3]
    todoist_api.tasks[category3.id] = [task4, task5]

    # Call the sync_new_month function
    sync_report = sync_new_month(todoist_api, "New Project", "Old Project")

    # Assert the expected results
    assert sync_report["old_project"] == "Old Project"
    assert sync_report["new_project"] == "New Project"
    assert sync_report["categories_synced"] == 3
    assert sync_report["tasks_moved"] == 2
    assert sync_report["tasks_copied"] == 3

    # Additional assertions for the synced data
    new_project = todoist_api.get_projects()[1]
    assert new_project.name == "New Project"

    new_categories = todoist_api.get_project_categories(new_project.id)
    assert len(new_categories) == 3
    assert new_categories[0].name == "Category 1"
    assert new_categories[1].name == "Category 2"
    assert new_categories[2].name == "Category 3_task"

    assert len(todoist_api.get_tasks(new_categories[0].id)) == 2
    assert len(todoist_api.get_tasks(new_categories[1].id)) == 1
    assert len(todoist_api.get_tasks(new_categories[2].id)) == 2