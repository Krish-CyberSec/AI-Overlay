import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set in the .env file."
    )

client = genai.Client(api_key=api_key)


def ask_ai(question: str) -> str:
    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=question,
    )

    return response.output_text