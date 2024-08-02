import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')
AUTHORIZED_TABLES_NAMES_STR = os.getenv('AUTHORIZED_TABLES_NAMES')
AUTHORIZED_TABLES_NAMES = AUTHORIZED_TABLES_NAMES_STR.split(",")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

