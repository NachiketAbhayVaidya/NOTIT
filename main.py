from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from ai_notes import generate_notes
from pdf_generator import create_pdf
import uuid
import os

app = FastAPI()

# Allow all platforms (Flutter Android / iOS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "running"}

@app.post("/generate-notes")
async def generate_notes_api(data: dict):
    topic = data.get("topic")
    if not topic:
        return {"error": "No topic provided"}

    notes_text = generate_notes(topic)

    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join("/tmp", filename)   # <-- IMPORTANT for cloud

    create_pdf(notes_text, filepath)

    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=f"{topic}.pdf"
    )
