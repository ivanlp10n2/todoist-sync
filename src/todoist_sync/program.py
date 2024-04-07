from typing import List, Dict
from todoist_sync.todoist_api import TodoistAPI, Project, Category, Task
from returns.maybe import Maybe
from returns.pipeline import flow
from returns.pointfree import bind, map_
from returns.result import Result, safe
from returns.curry import partial
from typing import Dict, Tuple
from returns.io import IO
from returns.future import FutureResult

@safe
def find_project_by_name(projects: List[Project], project_name: str)-> FutureResult[Project] :
    for project in projects:
        if project.name == project_name:
            return project
    return None

@safe
def create_new_project_if_not_exists(todoist_api: TodoistAPI, new_project_name: str, projects: List[Project])-> Project:
    new_project = find_project_by_name(projects, new_project_name).unwrap()
    return new_project if new_project else todoist_api.create_project(new_project_name)

def get_categories_and_tasks(todoist_api: TodoistAPI, project: Project)-> Tuple[List[Category], List[Task]]:
    old_categories = todoist_api.get_project_categories(project.id)
    return [(c, todoist_api.get_tasks(c.id)) for c in old_categories]

def create_sync_report(new_project_name: str, new_categories: List[Category], new_tasks: List[Task]) -> Dict[str, int]:
    # Your logic to compile the sync report based on new categories and tasks.
    pass

def sync_new_month(todoist_api: TodoistAPI, new_project_name: str, old_project_name: str) -> Result[Dict[str, int], Exception]:
    projects = todoist_api.get_projects()

    return flow(
        projects,
        bind(partial(find_project_by_name, project_name = old_project_name)),
        bind(partial(create_new_project_if_not_exists, todoist_api, new_project_name)),
        map_(lambda new_project: get_categories_and_tasks(todoist_api, new_project)),
        map_(lambda data: create_sync_report(new_project_name, *data))
    )