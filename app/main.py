from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from typing import List
import json
import logging
from pydantic import ValidationError
from fastapi import Form
from datetime import datetime

from app.database import create_supabase_client
from app.schemas import PetCreate, PetUpdate
from app.crud import get_all_pets, get_pet_by_id, create_pet, update_pet, delete_pet
from app.config import cloudinary

app = FastAPI(debug=True)

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

supabase = create_supabase_client()


async def upload_images(files: List[UploadFile]):
    uploaded_images = []
    for file in files:
        contents = await file.read()
        response = cloudinary.uploader.upload(contents, resource_type="image")
        uploaded_images.append({"url": response["secure_url"]})
    return uploaded_images


@app.get("/pets")
async def read_pets():
    try:
        pets = await get_all_pets(supabase)
        return pets
    except Exception as e:
        logger.error(f"Error reading pets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pets/{id}")
async def read_pet(id: str):
    try:
        pet = await get_pet_by_id(supabase, id)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return pet
    except Exception as e:
        logger.error(f"Error reading pet with id {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pets", status_code=201)
async def create_new_pet(pet: str = Form(...), files: List[UploadFile] = File(...)):
    """
    The 'pet' parameter expects a JSON string that matches the PetCreate structure: 
        type: PetType
        description: str
        name: str
        status: PetStatus
        location: str
        alive: bool
        contact: str
        date: datetime
    """
    try:
        pet_data = json.loads(pet)
        pet_data['date'] = datetime.fromisoformat(pet_data['date'])
        pet_obj = PetCreate(**pet_data)
        cloudinary_response = await upload_images(files)
        uploaded_image_json = json.dumps(cloudinary_response)
        new_pet = await create_pet(supabase, pet_obj, uploaded_image_json)
        return {"success": True, "message": "Pet created successfully"}
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        logger.error(f"Error creating pet: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@ app.put("/pets/{id}")
async def update_existing_pet(id: str, pet_update: PetUpdate):
    try:
        pet = await update_pet(supabase, id, pet_update.athome)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return {"success": True, "message": "Pet updated successfully"}
    except Exception as e:
        logger.error(f"Error updating pet with id {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@ app.delete("/pets/{id}")
async def delete_existing_pet(id: str):
    try:
        pet = await delete_pet(supabase, id)
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        return {"message": "Pet deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting pet with id {id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
