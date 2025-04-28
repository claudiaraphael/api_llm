from fastapi import FastAPI, Depends, HTTPException, Header
import os
import ollama
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
api_key = os.getenv("API_KEY")

# Middleware to check for API key
def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)

    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key, or no credits")
    return x_api_key

def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}

API_KEY_CREDITS = {
    api_key: 10,  # Example initial credits
}


