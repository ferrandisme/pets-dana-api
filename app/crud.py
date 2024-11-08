from sqlalchemy.orm import Session
from .models import Pet
from .schemas import PetCreate
import json
from datetime import datetime


async def get_all_pets(db: Session):
    return db.query(Pet).order_by(Pet.created_at.desc()).all()


async def get_pet_by_id(db: Session, id: str):
    return db.query(Pet).filter(Pet.id == id).first()


async def create_pet(db: Session, pet: PetCreate, uploaded_image_json: str):
    created_at = datetime.now()
    created_by = "web"
    new_pet = Pet(
        type=pet.type,
        images=uploaded_image_json,
        description=pet.description,
        name=pet.name,
        status=pet.status,
        location=pet.location,
        alive=pet.alive,
        contact=pet.contact,
        date=pet.date,
        created_by=created_by,
        created_at=created_at
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet


async def update_pet(db: Session, id: str, athome: bool):
    pet = db.query(Pet).filter(Pet.id == id).first()
    if pet:
        pet.atHome = athome
        db.commit()
    return pet


async def delete_pet(db: Session, id: str):
    pet = db.query(Pet).filter(Pet.id == id).first()
    if pet:
        db.delete(pet)
        db.commit()
    return pet
