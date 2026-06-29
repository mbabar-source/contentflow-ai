# os helps us read environemtn variables from the operating system.
import os

import json

# load_dotenv loads secret values fromthe .env file.
from dotenv import load_dotenv

from deepagents import create_deep_agent


# Load variables from the .env file.
load_dotenv()

def check_deepagents_ready():
    # Read the OpenAI API key from the environment.
    api_key= os.getenv("OPENAI_API_KEY")

    # If the key is missing DeepAgents cannot call the model.
    if not api_key:
        return {
            "status": "missing",
            "message": "OPENAI_API_KEY was not found. DeepAgents cannot run yet.",
        }
    return {
        "status": "ready",
        "message": "DeepAgents setup is ready to use the OpenAi API.",
    }

def run_simple_trend_agent(topic: str, sources:list):
    # Read the OpenAI API key from the environment.
    api_key = os.getenv("OPENAI_API_KEY")

    # If the key is missing, stop and show a clear error.
    if not api_key:
        raise ValueError("OPEN_API_KEY was not found. DeepAgent cannot run.")

    # Build context from the saved database sources.
    source_context = "\n\n".join(
        f"Source ID: {source.id}\n"
        f"Platform: {source.platform}\n"
        f"Title: {source.title}\n"
        f"Body: {source.body}"
        for source in sources
    )

    #  This prompt tells the agent what role it has and what steps it should follow.
    agent_instructions = """
You are a trend analysis agent for content creators.
Your Task:
1. Analyze the provided source discussions.
2. Identify repeated problems, questions or trends.
3. Suggest useful content angles for creators.
4. Explain your result clearly and practically.

Do not invent sources. Use only the provided source context.
    """

    # Create the DeepAgent
    agent = create_deep_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        system_prompt=agent_instructions,
    )

    # Ask the agent to analyze the topic and source context.
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content":  (
                        f"Topic: {topic}\n\n"
                        f"Source context:\n{source_context}\n\n"
                        "Analyze these sources and explain the main trend opportunities for content creators."
                    ),
                }
            ]
        }
    )
    # Return the final agent message.
    final_message = result["messages"][-1]

    if hasattr(final_message, "content"):
        return final_message.content

    return str(final_message)

def run_structured_trend_agent(topic: str, sources: list):

    # Read the OpenAI API key from the environment.
    api_key = os.getenv("OPENAI_API_KEY")

    # If the key is missing, stop and show a clear error.
    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found. DeepAgent cannot run.")

    # Collect source IDs so we know which sources were used.
    source_ids = ",".join(str(source.id) for source in sources)

    # Build context from the saved database sources.
    source_context = "\n\n".join(
        f"Source ID: {source.id}\n"
        f"Platform: {source.platform}\n"
        f"Title: {source.title}\n"
        f"Body: {source.body}"
        for source in sources
    )

    # This prompt tells the agent to return only JSON.
    agent_instructions = """
    You are a trend analysis agent for content creators.
    Analyze the provided source discussions and return one structured content idea.
    Return ONLY valid JSON.
    Do not use markdown.
    Do not use ```json.
    Do not add explanations outside the JSON.
    The JSON must have exactly these fields:
    {
      "title": "short attractive title",
      "summary": "clear summary of the trend",
      "trend_category": "main trend category",
      "linkedin_post_idea": "practical LinkedIn post idea",
      "youtube_video_idea": "practical YouTube video idea",
      "blog_article_idea": "practical blog article idea"
    }
    Do not invent sources. Use only the provided source context.
    """
    # Create the DeepAgent.
    agent = create_deep_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        system_prompt=agent_instructions,
    )

    # Ask the DeepAgent to generate structured JSON from the topic and source context.
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Topic: {topic}\n\n"
                        f"Source context:\n{source_context}\n\n"
                        "Generate one structured content idea as valid JSON."
                    ),
                }
            ]
        }
    )

    # Get the final agent message.
    final_message = result["messages"][-1]

    if hasattr(final_message, "content"):
        final_text = final_message.content
    else:
        final_text = str(final_message)

    # Convert the DeepAgent response into a Python dictionary.
    # Sometimes the DeepAgent returns JSON text.
    # Sometimes it returns a dictionary with the JSON inside a "text" field.
    # Sometimes it returns a list containing that dictionary.
    if isinstance(final_text, list):
        final_text = final_text[0]

    if isinstance(final_text, dict) and "text" in final_text:
        idea_data = json.loads(final_text["text"])
    elif isinstance(final_text, dict):
        idea_data = final_text
    else:
        idea_data = json.loads(final_text)

    # Add topic and source_ids because our database needs them too.
    idea_data["topic"] = topic
    idea_data["source_ids"] = source_ids

    return idea_data