import os
from dotenv import load_dotenv
from todoist_api import TodoistAPIImpl
from program import sync_new_month

def main():
    load_dotenv()  # Load environment variables from .env file
    
    api_key = os.getenv("TODOIST_API_KEY")
    if not api_key:
        raise ValueError("TODOIST_API_KEY not found in environment variables.")
    
    todoist_api = TodoistAPIImpl(api_key)
    
    new_project_name = "March 2024"
    old_project_name = "July 2023"
    
    try:
        sync_report = sync_new_month(todoist_api, new_project_name, old_project_name)
        print("Sync Report:")
        print(sync_report)
    except Exception as e:
        print(f"An error occurred during sync: {str(e)}")

if __name__ == "__main__":
    main()
