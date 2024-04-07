import os
from dotenv import load_dotenv

from dataclasses import dataclass

@dataclass
class Config:
    todoist_api_key: str
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.todoist_api_key = self.handleTodoistApiKey()

    def handleTodoistApiKey(self):
        config_key = "TODOIST_API_KEY"
        todoist_api_key = os.getenv(config_key)
        if not todoist_api_key:
            raise ValueError(f"{config_key} environment variable is not set")
        return todoist_api_key
