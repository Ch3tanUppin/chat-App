from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from backend.pdf_loader import load_pdf
import PyPDF2

app = FastAPI()

class Query(BaseModel):
    query: str

knowledge_base = {}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF.")
    
    pdf_reader = PyPDF2.PdfReader(file.file)
    pdf_text = []

    for page in pdf_reader.pages:
        pdf_text.append(page.extract_text())
    
    full_text = "\n".join(pdf_text)
    knowledge_base[file.filename] = full_text
    
    return {"filename": file.filename, "message": "PDF uploaded and text extracted successfully."}

@app.post("/query")
async def get_answer(query: Query):
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="No PDF uploaded.")

    relevant_texts = []
    
    for filename, text in knowledge_base.items():
        # Check if the query exists in the text
        if query.query.lower() in text.lower():
            # Add a snippet of text surrounding the query for context
            start_index = text.lower().find(query.query.lower())
            end_index = start_index + len(query.query) + 100  # 100 characters after the query
            
            snippet = text[start_index:end_index].strip()
            relevant_texts.append(f"Found in {filename}: {snippet}...")

    if not relevant_texts:
        return {"answer": "No relevant information found."}
    
    return {"answer": " | ".join(relevant_texts)}
