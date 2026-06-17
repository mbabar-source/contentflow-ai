# We import BaseModel from Pydantic.
# BaseModel is used to define the shape of request and response data.
from pydantic import BaseModel

# datetime is used because our database model has a created_at field.
from datetime import datetime

# Optional means the field can be empty / None.
from typing import Optional


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