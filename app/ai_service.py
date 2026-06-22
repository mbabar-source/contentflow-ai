# os helps us read environment variables from the operating system.
import os

# load_dotenv loads variables from the .env file into the environment.
from dotenv import load_dotenv


# Load variables from the .env file.
load_dotenv()


def check_openai_api_key():
    # Read the API key from the environment.
    api_key = os.getenv("OPENAI_API_KEY")

    # If the key is missing, return a helpful message.
    if not api_key:
        return {
            "status": "missing",
            "message": "OPENAI_API_KEY was not found. Please add it to your .env file.",
        }

    # If the key exists, do not print or return the real key.
    return {
        "status": "loaded",
        "message": "OPENAI_API_KEY is loaded successfully.",
    }