from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.models import PetType, PetStatus


class PetCreate(BaseModel):
    type: PetType
    description: str
    name: str
    status: PetStatus
    location: str
    alive: bool
    contact: str
    date: datetime


class PetUpdate(BaseModel):
    athome: bool
