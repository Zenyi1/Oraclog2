from fastapi import FastAPI, HTTPException
import uvicorn
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

app=FastAPI()

def ai_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction="You are an assistant",
            max_output_tokens=1024,
        )
    )
    return response.text

class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
async def root():
    return {"message": "LogOracle API caller"}

@app.post("/generate-response")
async def generate_response(request: PromptRequest):
    try:
        response = ai_response(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling the Gemini API: {e}")

port = 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
