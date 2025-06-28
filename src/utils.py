# config.py

import os
from dotenv import load_dotenv
load_dotenv()

def get_api_key():
    """
    Retrieves the Gemini API key from an environment variable.
    Raises an error if not set.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your environment.")
    return key

