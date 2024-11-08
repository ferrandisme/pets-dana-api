from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from typing import List
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.schemas import PetCreate, PetUpdate
from app.crud import get_all_pets, get_pet_by_id, create_pet, update_pet, delete_pet

app = FastAPI()


async def upload_images(files: List[UploadFile]):
    return [{"url": "http://example.com/image.jpg"}]


@app.get("/pets")
async def read_pets(db: Session = Depends(get_db)):
    try:
        pets = await get_all_pets(db)
        return pets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pets/{id}")
async def read_pet(id: str, db: Session = Depends(get_db)):
    try:
        pet = await get_pet_by_id(db, id)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return pet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pets", status_code=201)
async def create_new_pet(pet: PetCreate, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        cloudinary_response = await upload_images(files)
        uploaded_image_json = json.dumps(cloudinary_response)
        new_pet = await create_pet(db, pet, uploaded_image_json)
        return {"success": True, "message": "Pet created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/pets/{id}")
async def update_existing_pet(id: str, pet_update: PetUpdate, db: Session = Depends(get_db)):
    try:
        pet = await update_pet(db, id, pet_update.athome)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return {"success": True, "message": "Pet updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/pets/{id}")
async def delete_existing_pet(id: str, db: Session = Depends(get_db)):
    try:
        pet = await delete_pet(db, id)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return {"message": "Pet deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
