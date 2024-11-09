from supabase import Client, create_client
from app.config import supabase_api, supabase_url

api_url: str = supabase_url
key: str = supabase_api


def create_supabase_client():
    supabase: Client = create_client(api_url, key)
    return supabase
