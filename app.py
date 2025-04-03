from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# Set your DeepSeek API Key
DEEPSEEK_API_KEY = "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"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

app = FastAPI()

class UserInput(BaseModel):
    query: str

@app.get("/")  # This will handle requests to "/"
def home():
    return {"message": "FastAPI Chatbot is live on Render!"}

@app.get("/chat")
def chat():
    return {"message": "Chatbot API is ready!"}


@app.post("/chat")
def chat_with_model(user_input: UserInput):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-llm-r1",
        "messages": [{"role": "user", "content": user_input.query}]
    }
    
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return {"response": response.json()["choices"][0]["message"]["content"]}
    else:
        return {"error": "API request failed", "status_code": response.status_code}
