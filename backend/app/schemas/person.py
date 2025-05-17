from pydantic import BaseModel
from typing import Optional

class PersonCreate(BaseModel):
    name: str
    age: Optional[int]
    location: Optional[str]
    last_seen: Optional[str]

class PersonOut(BaseModel):
    id: int
    name: str
    age: Optional[int]
    location: Optional[str]
    last_seen: Optional[str]
    image_url: Optional[str]

    class Config:
        orm_mode = True