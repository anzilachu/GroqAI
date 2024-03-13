import os
import environ
from groq import Groq

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def get_groq_client():
    api_key = env('GROQ_API_KEY')
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable")
    return Groq(api_key=api_key)