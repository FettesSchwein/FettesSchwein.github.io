from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Chatbot is live on Render!"}

@app.get("/chat/")
def chat_get():
    return {"message": "Use a POST request to send messages."}

@app.post("/chat/")
def chat_post(query: dict):
    user_message = query.get("message")

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    return {"response": f"Chatbot received: {user_message}"}
