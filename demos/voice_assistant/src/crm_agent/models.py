import uuid
from pydantic import BaseModel, Field
from typing import List, Optional


class Listing(BaseModel):
    address: str

class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:5])
    name: str
    # email: str
    phone: str
    notes: list[str] = Field(default_factory=list)
    collection: list[Listing] = Field(default_factory=list)
