import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
api = os.getenv("SUPABASE_ANON_KEY")

if not url or not api:
    raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY is not set")
