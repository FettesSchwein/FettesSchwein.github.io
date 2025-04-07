from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store chat history in memory (can be replaced with DB for persistence)
chat_history = []

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def post_chat(req: ChatRequest):
    user_input = req.message

    # Add user message to history
    chat_history.append({"role": "user", "content": user_input})

    # Keep the last 10 messages for context
    context = chat_history[-10:]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a helpful assistant."}] + context
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return JSONResponse(content={"response": reply})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
