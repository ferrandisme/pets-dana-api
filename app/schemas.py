from pydantic import BaseModel
from datetime import datetime
from typing import List


class PetCreate(BaseModel):
    type: str
    description: str
    name: str
    status: str
    location: str
    alive: bool
    contact: str
    date: datetime
    images: List[str] = []


class PetUpdate(BaseModel):
    athome: bool
