# ContentFlow AI

ContentFlow AI is an AI-powered trend and content idea generator for influencers, creators, freelancers, and small businesses.

## Main User Flow

Enter topic → collect sources → generate content ideas

## Current Phase


Phase 10 completed: Tavily online source collection is connected to the AI idea generation workflow.

The app can now:

* receive a topic from the user,
* check if sources already exist in the database,
* collect online sources with Tavily if no sources exist,
* save online sources into the sources table,
* send saved sources to OpenAI as RAG context,
* generate structured content ideas,
* save the AI result into the trend_ideas table.

## Tech Stack

- FastAPI
- Uvicorn
- Python
- SQLite
- SQLAlchemy
- OpenAI API
- Tavily API
- RAG
- Structured Output
- Jinja2 frontend later
- Git and GitHub

## How to Run

```bash
uvicorn app.main:app --reload

