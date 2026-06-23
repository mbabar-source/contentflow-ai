from app.ai_service import check_openai_api_key, generate_ai_content_idea
# We import FastAPI from the fastapi package.
# FastAPI is the framework that helps us create API endpoints.
from fastapi import FastAPI, Depends, HTTPException

# Session is used for type hints for database sessions.
from sqlalchemy.orm import Session

# We import our database setup to check that the database connection code works.
from app.database import Base, engine, SessionLocal

# We import models so SQLAlchemy knows which tables exist.
from app import models

# We import schemas for request and response validation.
from app import schemas

from app.online_collector import check_tavily_api_key, collect_online_sources

# This creates the database tables from our SQLAlchemy models.
# If the tables already exist, SQLAlchemy will not create them again.
Base.metadata.create_all(bind=engine)

# This function creates a database session for each request.
# It gives the endpoint access to the database and closes the session after the request is finished.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# This function simulates automatic source collection.
# Later, we can replace this with real Reddit, forum, or web API collection.
def simulate_source_collection(topic: str):
    return [
        {
            "title": f"People are asking for better ideas about {topic}",
            "body": f"Many users say they struggle to find fresh and useful content ideas about {topic}. They want simple, practical, and engaging post ideas.",
            "source_url": "https://example.com/reddit-style-post",
            "platform": "Reddit",
            "topic": topic,
        },
        {
            "title": f"Common problems beginners face with {topic}",
            "body": f"Forum discussions show that beginners interested in {topic} often feel overwhelmed and do not know where to start.",
            "source_url": "https://example.com/forum-style-post",
            "platform": "Forum",
            "topic": topic,
        },
        {
            "title": f"Trending content opportunities in {topic}",
            "body": f"Blog-style content suggests that audiences are looking for clear tips, personal stories, mistakes to avoid, and step-by-step guidance about {topic}.",
            "source_url": "https://example.com/blog-style-post",
            "platform": "Blog",
            "topic": topic,
        },
    ]


# This function creates a beginner-friendly fake AI result.
# Later, we will replace this with a real OpenAI API call.
def generate_fake_content_idea(topic: str, sources: list[models.Source]):
    # Collect source IDs so we know which saved sources helped create this idea.
    source_ids = ",".join(str(source.id) for source in sources)

    # Create a structured idea using the topic and saved source discussions.
    return {
        "topic": topic,
        "title": f"Content opportunities around {topic}",
        "summary": f"Based on saved source discussions, people are looking for practical, simple, and useful guidance about {topic}.",
        "trend_category": "Content Inspiration",
        "linkedin_post_idea": f"Write a LinkedIn post about the common problems people face with {topic} and share 3 practical lessons.",
        "youtube_video_idea": f"Create a YouTube video titled: Beginner-friendly guide to {topic}: problems, trends, and content ideas.",
        "blog_article_idea": f"Write a blog article explaining what people are discussing about {topic} and how creators can turn those discussions into content.",
        "source_ids": source_ids,
    }


# Here we create the FastAPI application object.
# This "app" object is the main entry point of our backend.
app = FastAPI(
    title="ContentFlow AI",
    description="AI-powered trend and content idea generator.",
    version="0.1.0",
)


# This is our first API endpoint
# @app.get("/") means: when someone visits the homepage URL with a get request
# run the function below.
@app.get("/")
def read_root():
    # FastAPI automatically converts this python dictionary into JSON.
    return {

        "message": "Welcome to ContentFlow AI",

        "status": "Phase 1 setup is working",

        "next_step": "Database, AI, RAG, and frontend will be added later",

    }

# This is a health check endpoint.
#  It is used to check if the backend server is running correctly.

@app.get("/health")
def health_check():
    # This reponse tell us that the backend is alive and working.
    return {
        "status": "ok",
        "message": "ContentFlow AI backend is running"
    }

# This endpoint creates a new source and saves it into the database.
@app.post("/sources", response_model=schemas.SourceResponse)
def create_source(
    source: schemas.SourceCreate,
    db: Session = Depends(get_db)
):
    # Create a new Source database object using the data from the request body.
    new_source = models.Source(
        title=source.title,
        body=source.body,
        source_url=source.source_url,
        platform=source.platform,
        topic=source.topic,
    )

    # Add the new source object to the database session.
    db.add(new_source)

    # commit saves the new source permanently into the database.
    db.commit()

    # Refresh updates the python object with database-generated values like id and created at.
    db.refresh(new_source)

    # Return the saved source as the API response.
    return new_source

@app.get("/sources", response_model=list[schemas.SourceResponse])
def get_sources(db: Session = Depends(get_db)):
    # Query the sources table and return all rows.
    sources = db.query(models.Source).all()

    #FastAPI converts the list of database objects into JSON
    return sources

# This endpoint automatically collects simulated sources for a topic
# and saves them into the database.
@app.post("/collect-sources", response_model=list[schemas.SourceResponse])
def collect_sources(
    request: schemas.TopicRequest,
    db: Session = Depends(get_db)
):
    # Step 1: Get the topic from the request body.
    topic = request.topic

    # Step 2: Simulate collecting source posts related to the topic.
    collected_sources = simulate_source_collection(topic)

    # Step 3: Create an empty list to store the saved database objects.
    saved_sources = []

    # Step 4: Loop through each collected source dictionary.
    for source_data in collected_sources:
        # Convert the dictionary into a SQLAlchemy Source object
        new_source = models.Source(
            title=source_data["title"],
            body=source_data["body"],
            source_url=source_data["source_url"],
            platform=source_data["platform"],
            topic=source_data["topic"],
        )

        # Add the new source to the database session.
        db.add(new_source)

        # save this object in our list so we can return it later.
        saved_sources.append(new_source)

    # step5: commit once after adding all sources.
    # This saves all collected sources permenantly.
    db.commit()

    # Step 6: Refresh each saved source so it gets id and created_at.
    for source in saved_sources:
        db.refresh(source)

    # Step 7: Return the saved sources.
    return saved_sources


# This endpoint reads all generated trend ideas from the database.
@app.get("/trend-ideas", response_model=list[schemas.TrendIdeaResponse])
def get_trend_ideas(db: Session = Depends(get_db)):
    # Query the trend_ideas table and return all rows.
    trend_ideas = db.query(models.TrendIdea).all()

    # FastAPI converts the list of database objects into JSON.
    return trend_ideas


# This endpoint generates content ideas for a topic.
# It first checks saved sources. If no sources exist, it collects online sources with Tavily automatically.
@app.post("/generate-ideas",
response_model=schemas.TrendIdeaResponse)
def generate_ideas(
    request: schemas.TopicRequest,
    db: Session = Depends(get_db)
):
    # Step 1: Get the topic from the request body.
    topic = request.topic

    # Step 2: Search the database for existing sources with this topic.
    existing_sources = db.query(models.Source).filter(
        models.Source.topic == topic
    ).all()

    # Step 3: If no sources exist for this topic, collect real online sources with Tavily automatically.
    if not existing_sources:
        try:
            collected_sources = collect_online_sources(topic)
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Online source collection failed: {error}")

        if not collected_sources:
            raise HTTPException(status_code=404, detail="No online sources were found for this topic.")

        saved_sources = []

        for source_data in collected_sources:
            new_source = models.Source(
                title=source_data["title"],
                body=source_data["body"],
                source_url=source_data["source_url"],
                platform=source_data["platform"],
                topic=source_data["topic"],
            )

            db.add(new_source)
            saved_sources.append(new_source)

        db.commit()

        for source in saved_sources:
            db.refresh(source)

        sources_for_idea = saved_sources
    else:
        # Step 4: If sources already exist, use them for idea generation.
        sources_for_idea = existing_sources

    # Step 5: Generate a structured AI result using the retrieved sources.
    # This is our first real RAG + OpenAI step.
    try:
        idea_data = generate_ai_content_idea(topic, sources_for_idea)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    # Step 6: Convert the generated idea into a SQLAlchemy TrendIdea object.
    new_trend_idea = models.TrendIdea(
        topic=idea_data["topic"],
        title=idea_data["title"],
        summary=idea_data["summary"],
        trend_category=idea_data["trend_category"],
        linkedin_post_idea=idea_data["linkedin_post_idea"],
        youtube_video_idea=idea_data["youtube_video_idea"],
        blog_article_idea=idea_data["blog_article_idea"],
        source_ids=idea_data["source_ids"],
    )

    # Step 7: Save the generated trend idea into the database.
    db.add(new_trend_idea)
    db.commit()
    db.refresh(new_trend_idea)

    # Step 8: Return the saved trend idea.
    return new_trend_idea

# This endpoint checks whether the OpenAI API key is loaded.
# it does not show the real key for security reasons.

@app.get("/check-openai-key")
def check_openai_key():
    return check_openai_api_key()

# This endpoint checks whether the Tavily API key is loaded.
@app.get("/check-tavily-key")
def check_tavily_key():
    return check_tavily_api_key()

# This endpoint tests online source collection with Tavily.
# It does not save anything to the database yet.
@app.post("/test-online-sources")
def test_online_sources(request: schemas.TopicRequest):
    online_sources = collect_online_sources(request.topic)
    return {
        "topic": request.topic,
        "source_count": len(online_sources),
        "sources": online_sources,
    }