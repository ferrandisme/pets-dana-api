import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_api = os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_api:
    raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY is not set")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

config = cloudinary.config()

if not config.cloud_name or not config.api_key or not config.api_secret:
    raise ValueError(
        "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY or CLOUDINARY_API_SECRET is not set")
