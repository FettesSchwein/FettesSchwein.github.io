import requests
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ HEAD request fix for Render
@app.get("/")
@app.head("/")
def root():
    return {"message": "API is live"}

# ✅ Define input model for POST request
class UserInput(BaseModel):
    query: str

# ✅ Load DeepSeek API Key (Ensure this is set in Render environment variables)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Set this in Render’s environment settings

# ✅ POST request to handle chatbot input
@app.post("/chat")
def chat(user_input: UserInput):
    if not DEEPSEEK_API_KEY:
        return {"error": "DeepSeek API key is missing!"}

    # DeepSeek API URL
    url = "https://api.deepseek.com/v1/chat/completions"

    # Construct API request
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input.query}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    # Make API call
    response = requests.post(url, json=payload, headers=headers)

    # Handle response
    if response.status_code == 200:
        response_data = response.json()
        return {"response": response_data["choices"][0]["message"]["content"]}
    else:
        return {"error": f"DeepSeek API Error: {response.text}"}
