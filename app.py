from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

# Replace this with your actual DeepSeek API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

@app.get("/")
def home():
    return {"message": "FastAPI Chatbot is live on Render!"}

@app.post("/chat/")
def chat(query: dict):
    user_message = query.get("message")
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek-r1",  # Use the correct model name
        "messages": [{"role": "user", "content": user_message}],
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
