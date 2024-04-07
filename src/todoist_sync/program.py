from typing import List, Dict
from todoist_sync.todoist_api import TodoistAPI, Project, Category, Task
from returns.maybe import Maybe

def sync_new_month(todoist_api: TodoistAPI, new_project_name: str, old_project_name: str) -> Dict[str, int]:
    try:
        projects = todoist_api.get_projects()
        old_project = next((p for p in projects if p.name == old_project_name), None)
        if not old_project:
            raise ValueError(f"Old project '{old_project_name}' not found.")
        
        new_project = next((p for p in projects if p.name == new_project_name), None)
        if not new_project:
            new_project = todoist_api.create_project(new_project_name)
        
        old_categories = todoist_api.get_project_categories(old_project.id)
        new_categories: List[Category] = []
        
        for old_category in old_categories:
            new_category = todoist_api.create_category(new_project.id, old_category.name)
            new_categories.append(new_category)
            
            old_tasks = todoist_api.get_tasks(old_category.id)
            print(f"Old category: {old_category.name}")
            print(f"Number of old tasks: {len(old_tasks)}")
            
            for old_task in old_tasks:
                if old_category.name.endswith("_task"):
                    todoist_api.move_task(old_task.id, new_category.id)
                else:
                    todoist_api.copy_task(old_task.id, new_category.id)
            
            print(f"New category: {new_category.name}")
            print(f"Number of new tasks: {len(todoist_api.get_tasks(new_category.id))}")
            print("---")
        
        tasks_moved = sum(len(todoist_api.get_tasks(c.id)) for c in new_categories if c.name.endswith("_task"))
        print(f"Total tasks moved: {tasks_moved}")
        
        sync_report = {
            "old_project": old_project_name,
            "new_project": new_project_name,
            "categories_synced": len(new_categories),
            "tasks_moved": tasks_moved,
            "tasks_copied": sum(len(todoist_api.get_tasks(c.id)) for c in new_categories if not c.name.endswith("_task")),
        }
        
        return sync_report
    
    except Exception as e:
        raise RuntimeError(f"Error occurred during sync: {str(e)}") from e