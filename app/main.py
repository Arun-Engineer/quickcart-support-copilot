# app/main.py

from fastapi import FastAPI, HTTPException
from app.models import ChatRequest
from app.llm_client import ask_llm

app = FastAPI(title = "Quickcart Support Copilot")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    result = ask_llm(request.question)
    if result["error"] is not None:
        raise HTTPException(status_code = 503, detail = result)
    return result