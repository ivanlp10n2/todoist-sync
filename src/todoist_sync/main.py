import os
from todoist_sync.config import Config
from todoist_sync.todoist_api import TodoistAPIImpl
from todoist_sync.program import sync_new_month

def main():
    configs = Config()
    
    todoist_api = TodoistAPIImpl(configs.todoist_api_key)
    
    new_project_name = "March 2024"
    old_project_name = "July 2023"
    zz = sync_new_month(todoist_api, new_project_name, old_project_name)
    
    try:
        sync_report = zz
        print("Sync Report:")
        print(sync_report)
    except Exception as e:
        print(f"An error occurred during sync: {str(e)}")

if __name__ == "__main__":
    main()
