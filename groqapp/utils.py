import os
from groq import Groq

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY environment variable")
    return Groq(api_key=api_key)
