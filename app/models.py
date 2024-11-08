from sqlalchemy import Column, String, Boolean, JSON, Text, Enum, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import enum


class PetType(enum.Enum):
    Perro = "Perro"
    Gato = "Gato"
    Otro = "Otro"


class PetStatus(enum.Enum):
    lost = "lost"
    found = "found"


class Pet(Base):
    __tablename__ = "pets"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=func.gen_random_uuid())
    type = Column(Enum(PetType), nullable=False)
    images = Column(JSON)
    description = Column(Text)
    name = Column(Text)
    status = Column(Enum(PetStatus), nullable=False)
    location = Column(Text, nullable=False)
    alive = Column(Boolean, default=True)
    contact = Column(Text, nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False)
    atHome = Column(Boolean, default=False)
    created_by = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
