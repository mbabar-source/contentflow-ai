# We import FastAPI from the fastapi package.
# FastAPI is the framework that helps us create API endpoints.
from fastapi import FastAPI, Depends

# Session is used for type hints for database sessions.
from sqlalchemy.orm import Session

# We import our database setup to check that the database connection code works.
from app.database import Base, engine, SessionLocal

# We import models so SQLAlchemy knows which tables exist.
from app import models

# We import schemas for request and response validation.
from app import schemas

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