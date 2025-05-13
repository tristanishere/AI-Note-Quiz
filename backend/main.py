from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import shutil, os

from transcribe import transcribe
from extract_text import extract_text_from_file
from summarizer import summarize_text, extract_keywords
from quizgen import generate_cloze_questions

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TextPath(BaseModel):
    path: str

class QuizBody(BaseModel):
    text: str

@app.post("/transcribe")
async def transcribe_endpoint(audio: UploadFile = File(...)):
    dest = f"{UPLOAD_DIR}/{audio.filename}"
    with open(dest, "wb") as f:
        shutil.copyfileobj(audio.file, f)
    text = transcribe(dest)
    return {"text": text}

@app.post("/extract")
def extract_endpoint(req: TextPath):
    text = extract_text_from_file(req.path)
    return {"text": text}

@app.post("/summarize")
def summarize_endpoint(req: TextPath):
    with open(req.path, "r", encoding="utf-8") as f:
        txt = f.read()
    return {
        "summary": summarize_text(txt),
        "keywords": extract_keywords(txt),
    }

@app.post("/quiz")
def quiz_endpoint(req: QuizBody):
    qs = generate_cloze_questions(req.text)
    return {"questions": qs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

