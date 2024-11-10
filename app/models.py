from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
import enum


class PetType(str, enum.Enum):
    Perro = "Perro"
    Gato = "Gato"
    Otro = "Otro"


class PetStatus(str, enum.Enum):
    lost = "lost"
    found = "found"


class Pet(BaseModel):
    id: str
    type: PetType
    images: List[Dict[str, str]]
    description: str
    name: str
    status: PetStatus
    location: str
    alive: bool
    contact: str
    date: datetime
    athome: bool
    created_by: str
    created_at: datetime
