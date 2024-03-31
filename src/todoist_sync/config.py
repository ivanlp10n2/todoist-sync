import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
