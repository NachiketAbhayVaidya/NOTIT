from fastapi import FastAPI
from fastapi.responses import FileResponse
from ai_notes import generate_notes
from pdf_generator import create_pdf
import uuid
import os

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "running"}

@app.get("/generate-notes/ping")
def ping2():
    return {"status": "running"}

# NEW: Fix Railway health check
@app.get("/generate-notes/ping")
def ping2():
    return {"status": "running"}

@app.post("/generate-notes")
async def generate_notes_api(data: dict):
    topic = data.get("topic")
    if not topic:
        return {"error": "No topic provided"}

    notes_text = generate_notes(topic)

    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(".", filename)

    create_pdf(notes_text, filepath)

    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=f"{topic}.pdf"
    )

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )
