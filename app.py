from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from rag_utils import load_dataset, build_faiss_index
import os
from openai import OpenAI
import faiss
import numpy as np

# Load env vars and client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load Excel dataset + index
df = load_dataset("trainingdataset_shrunk.xlsx")
index, text_chunks = build_faiss_index(df)

class ChatRequest(BaseModel):
    message: str

chat_history = []

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def post_chat(req: ChatRequest):
    user_input = req.message
    chat_history.append({"role": "user", "content": user_input})
    context = chat_history[-10:]

    # Step 1: Embed user query
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=[user_input]
    ).data[0].embedding

    # Step 2: Search FAISS
    D, I = index.search(np.array([query_embedding]).astype("float32"), k=3)
    relevant_chunks = [text_chunks[i] for i in I[0]]

    # Step 3: Prompt GPT-4o
    system_prompt = "You are a helpful assistant answering based on the following data rows:\n" + "\n".join(relevant_chunks)
    messages = [{"role": "system", "content": system_prompt}] + context

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return JSONResponse(content={"response": reply})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
