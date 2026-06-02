from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from src.rag import get_answer
load_dotenv()
app = FastAPI()
class Question(BaseModel):
    text: str
@app.post("/ask")
def ask(question:Question):
    answer = get_answer(question.text)
    return{"answer":answer}
