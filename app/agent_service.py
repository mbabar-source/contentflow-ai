# os helps us read environemtn variables from the operating system.
import os

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

