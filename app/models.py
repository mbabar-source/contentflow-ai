# We import Column and data types from SQLAlchemy
# These help us define the columns of our database tables
from sqlalchemy import Column, Integer, String, Text, DateTime

# datetime helps us save the creation of time each row.
from datetime import datetime

# We import Base from our database setup.
# Every table model will inherit from Base.
from app.database import Base

class Source(Base):
    # __tablename__ defines the real table name inside SQLite
    __tablename__ = "sources"

    # id is the primary key (Unique ID)
    id = Column(Integer, primary_key=True, index=True)

    # Title of the source post/article.
    title = Column(String, nullable=False)

    # main text/body of the source.
    body = Column(Text, nullable=False)

    # Optional URL of the Source
    source_url = Column(String, nullable=True)

    # Platform name, for example Reddit, Forum, Blog.
    platform = Column(String, nullable=False)

    # Topic entered by the user, for example skincare, fitness, AI tools.
    topic = Column(String, nullable=False, index=True)

    # Creation data/time
    created_at = Column(DateTime, default=datetime.utcnow)

class TrendIdea(Base):
    # __tablename__ defines the real table name inside SQLite.
    __tablename__ = "trend_ideas"

    # Unique ID for each generated trend idea.
    id = Column(Integer, primary_key=True, index=True)

    # The Topic used for idea generation.
    topic = Column(String, nullable=False, index=True)

    # AI-generated Title.
    title = Column(String, nullable=False)

    # AI-generated summary.
    summary = Column(Text, nullable=False)

    # Trend category, for example Beauty, Marketing, Fitness, Tech.
    trend_category = Column(String, nullable=False)

    # AI-generated LinkedIN content idea.
    linkedin_post_idea = Column(Text, nullable=False)

    # AI-generated YouTube content idea.
    youtube_video_idea = Column(Text, nullable=False)

    # AI-generated blog article idea.
    blog_article_idea = Column(Text, nullable=False)

    # Source IDs used by the AI.
    # For beginner version, we save them as text like "1,2,3".
    source_ids = Column(String, nullable=True)

    # Creation date/time.
    created_at = Column(DateTime, default=datetime.utcnow)
