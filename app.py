# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai

load_dotenv()

# NEW: use OpenAI class from openai v1+
client = openai.OpenAI(api_key="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")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def post_chat(data: ChatRequest):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": data.message}
            ]
        )
        reply = chat_completion.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"

    return JSONResponse(content={"response": reply})
