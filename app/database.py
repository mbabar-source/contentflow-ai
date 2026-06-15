# We import the SQLAlchemy tools needed to connect to a database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# This is the database URL.
# sqlite:/// means we are using a SQLite database file.
# contentflow.db will be the name of our database file.
DATABASE_URL = "sqlite:///./contentflow.db"


# The engine is the connection point between SQLAlchemy and the database.
# connect_args is needed for SQLite when using FastAPI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# SessionLocal creates database sessions.
# A session is like a temporary conversation between Python and the database.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base is the parent class for our future database tables.
# Later, our models like Source and TrendIdea will inherit from Base.
Base = declarative_base()