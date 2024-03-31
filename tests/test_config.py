import os
import pytest
from dotenv import load_dotenv

def test_todoist_api_key_loaded():
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("TODOIST_API_KEY")
    assert api_key is not None, "TODOIST_API_KEY not found in environment variables."
