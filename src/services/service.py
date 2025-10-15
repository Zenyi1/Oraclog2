from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def ai_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction="You are an assistant",
            max_output_tokens=1024,
        )
    )
    return response.text