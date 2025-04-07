from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Allow local JS fetch() access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global memory (basic version) - maps client IP to conversation
chat_memory = {}

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    client_ip = request.client.host
    history = chat_memory.get(client_ip, [])
    
    # Add new user message to history
    history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *history
            ]
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        chat_memory[client_ip] = history  # Save updated history

    except Exception as e:
        reply = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": reply,
        "user_input": user_input
    })
