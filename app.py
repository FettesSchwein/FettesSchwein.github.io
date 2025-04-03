from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Fix "HEAD /" issue
@app.get("/")
@app.head("/")
def root():
    return {"message": "API is live"}

# ✅ Ensure your chatbot endpoint exists and works
class UserInput(BaseModel):
    query: str

@app.post("/chat")
def chat(user_input: UserInput):
    response = f"Received: {user_input.query}"  # Replace with actual processing
    return {"response": response}
