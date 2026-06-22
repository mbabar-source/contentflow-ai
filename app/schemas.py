# We import BaseModel from Pydantic.
# BaseModel is used to define the shape of request and response data.
from pydantic import BaseModel

# datetime is used because our database model has a created_at field.
from datetime import datetime

# Optional means the field can be empty / None.
from typing import Optional

class TopicRequest(BaseModel):
    # This schema is used when the user sends only a topic.
    # Example: {"topic":"content creation")
    topic: str

class SourceCreate(BaseModel):
    # This schema defines what data the user must send when creating a new source
    title: str
    body: str
    source_url: Optional[str] = None
    platform: str
    topic: str

class SourceResponse(BaseModel):
    # This schema defines what data our API returns
    # after reading a source from the database
    id: int
    title: str
    body: str
    source_url: Optional[str] = None
    platform: str
    topic: str
    created_at: datetime

    # This setting allows pydantic to read data from SQLAlchemy objects.
    model_config = {
        "from_attributes": True
    }

class TrendIdeaResponse(BaseModel):
    # This schema defines what our API returns after reading or generating a trend idea.
    id: int
    topic: str
    title: str
    summary: str
    trend_category: str
    linkedin_post_idea: str
    youtube_video_idea: str
    blog_article_idea: str
    source_ids: Optional[str] = None
    created_at: datetime

    # This setting allows Pydantic to read data from SQLAlchemy objects.
    model_config = {
        "from_attributes": True
    }
