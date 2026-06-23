# os helps us read environment variables from the operating system.
import os

# json helps us convert the AI JSON text into a Python dictionary.
import json

# OpenAI is the official Python client for calling the OpenAI API.
from openai import OpenAI

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


def generate_ai_content_idea(topic: str, sources: list):
    # Read the OpenAI API key from the environment.
    api_key = os.getenv("OPENAI_API_KEY")

    # If the key is missing, stop and show a safe error.
    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found. Please add it to your .env file.")

    # Create the OpenAI client using the API key.
    client = OpenAI(api_key=api_key)

    # Get model name from environment, or use a default model.
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Collect source IDs so we know which saved sources helped create this idea.
    source_ids = ",".join(str(source.id) for source in sources)

    # Build RAG context from the database sources.
    # RAG means: retrieve saved sources and give them to the AI as context.
    source_context = "\n\n".join(
        f"Source ID: {source.id}\n"
        f"Platform: {source.platform}\n"
        f"Title: {source.title}\n"
        f"Body: {source.body}"
        for source in sources
    )

    # Ask the AI to analyze the retrieved sources and return structured JSON.
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI trend analyst for content creators. "
                    "Analyze the provided source discussions and generate practical content ideas. "
                    "Focus on recurring problems, questions, trends, and useful creator angles."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {topic}\n\n"
                    f"Retrieved source discussions from the database:\n{source_context}\n\n"
                    "Create one structured trend/content idea for content creators."
                ),
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "trend_content_idea",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "A short attractive title for the trend/content opportunity."
                        },
                        "summary": {
                            "type": "string",
                            "description": "A clear summary of what people are discussing and why it matters."
                        },
                        "trend_category": {
                            "type": "string",
                            "description": "The main category of the trend, for example Beauty, Marketing, AI, Fitness, or Lifestyle."
                        },
                        "linkedin_post_idea": {
                            "type": "string",
                            "description": "A practical LinkedIn post idea based on the trend."
                        },
                        "youtube_video_idea": {
                            "type": "string",
                            "description": "A practical YouTube video idea based on the trend."
                        },
                        "blog_article_idea": {
                            "type": "string",
                            "description": "A practical blog article idea based on the trend."
                        }
                    },
                    "required": [
                        "title",
                        "summary",
                        "trend_category",
                        "linkedin_post_idea",
                        "youtube_video_idea",
                        "blog_article_idea"
                    ],
                    "additionalProperties": False
                }
            }
        },
    )

    # The AI response is JSON text, so we convert it into a Python dictionary.
    ai_data = json.loads(response.choices[0].message.content)

    # Add fields that come from our app/database, not from the AI.
    ai_data["topic"] = topic
    ai_data["source_ids"] = source_ids

    return ai_data