from supabase import Client
from app.schemas import PetCreate
from app.models import Pet
import json
from datetime import datetime


async def get_all_pets(supabase: Client):
    response = supabase.table("pets").select(
        "*").order("created_at", desc=True).execute()
    pets_data = response.data

    pets = []
    for pet_data in pets_data:
        if isinstance(pet_data['images'], str):
            pet_data['images'] = json.loads(pet_data['images'])

        if 'atHome' not in pet_data:
            pet_data['atHome'] = False

        pet = Pet(**pet_data)
        pets.append(pet)

    return pets


async def get_pet_by_id(supabase: Client, id: str):
    response = supabase.table("pets").select(
        "*").eq("id", id).single().execute()
    pet_data = response.data

    if isinstance(pet_data['images'], str):
        pet_data['images'] = json.loads(pet_data['images'])

    if 'atHome' not in pet_data:
        pet_data['atHome'] = False

    pet = Pet(**pet_data)
    return pet


async def create_pet(supabase: Client, pet: PetCreate, uploaded_image_json: str):
    created_at = datetime.now().isoformat()
    created_by = "web"
    new_pet = {
        "type": pet.type,
        "images": json.loads(uploaded_image_json),
        "description": pet.description,
        "name": pet.name,
        "status": pet.status,
        "location": pet.location,
        "alive": pet.alive,
        "contact": pet.contact,
        "date": pet.date.isoformat(),
        "created_by": created_by,
        "created_at": created_at
    }
    response = supabase.table("pets").insert(new_pet).execute()
    return response.data


async def update_pet(supabase: Client, id: str, atHome: bool):
    response = supabase.table("pets").update(
        {"atHome": atHome}).eq("id", id).execute()
    return response.data


async def delete_pet(supabase: Client, id: str):
    response = supabase.table("pets").delete().eq("id", id).execute()
    return response.data
