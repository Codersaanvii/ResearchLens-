from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from rag import get_answer_stream,build_db
load_dotenv()
app = FastAPI()
db_store ={}

@app.post("/upload")
async def upload_pdf(file:UploadFile = File(...)):
    """upload a pdf and build its vector db"""
    db = build_db(file.file)
    db_store["current"]=db
    return {"status": "PDF processed", "filename": file.filename}

class Question(BaseModel):
    text: str
@app.post("/ask")
async def ask_question(question:Question):
    """Ask a question about the most recently uploaded PDF, streamed back."""
    db = db_store.get("current")
    if db is None:
        return{"error":"No PDF uploaded yet"}
    async def stream_generator():
        for chunk in get_answer_stream(question.text,db):
            yield chunk
    return StreamingResponse(strean_generator(),media_type = "text/plain")
