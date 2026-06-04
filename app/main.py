# We import FastAPI from the fastapi package.
# FastAPI is the framework that helps us create API endpoints.
from fastapi import FastAPI

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
