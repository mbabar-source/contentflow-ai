# os helps us read environment variables from the operating system.
import os

# TavilyClient lets us search online using the Tavily API.
from tavily import TavilyClient

# load_dontenv loads secret values from the .env file.
from dotenv import load_dotenv

#load environment variables from .env.
load_dotenv()

def check_tavily_api_key():
    # Read the Tavily API key from the environment
    api_key = os.getenv("TAVILY_API_KEY")

    # If the key is missing, return a helpful message.
    if not api_key:
        return {
            "status": "missing",
            "message": "TAVILY_API_KEY was not found. please add it."
        }

    # If the key exists, do not return the real key.
    return{
        "status": "loaded",
        "message": "TAVILY_API_KEY is loaded successfully."
    }

def collect_online_sources(topic:str):
    # Read the Tavily API key from the environment.
    api_key = os.getenv("TAVILY_API_KEY")

    # If the key is missing, stop the function and show a clear error.
    if not api_key:
        raise ValueError("TAVILY_API_KEY was not found")

    # Create a Tavily client using the API key.
    tavily_client = TavilyClient(api_key=api_key)

    # Create a search query for content discussions around the topic.
    search_query = f"{topic} common problems trends discussions content ideas."

    # Search online using Tavily.
    response = tavily_client.search(
        query=search_query,
        max_results=3,
        include_answer=False,
        include_raw_content=False,
    )

    # Tavily returns results inside the "results" key.+
    results = response.get("results", [])

    # This list will store our cleaned source dictionaries.
    collected_sources = []

    # Loop through each online result and convert it into our source
    for result in results:
        source = {
            "title": result.get("title", "Untitled source"),
            "body": result.get("content", "No content available."),
            "source_url": result.get("url"),
            "platform": "Tavily Search",
            "topic": topic,
        }

        collected_sources.append(source)

        # Return the cleaned list of source dictionaries.
        return collected_sources