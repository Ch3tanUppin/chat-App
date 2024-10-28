# backend/api.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import PyPDF2
import os

app = FastAPI()

class Query(BaseModel):
    query: str

knowledge_base = {}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Ensure the uploaded file is a PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF.")

        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(file.file)
        pdf_text = []
        
        # Extract text from each page of the PDF
        for page in pdf_reader.pages:
            pdf_text.append(page.extract_text())
        
        # Combine the text into a single string
        full_text = "\n".join(pdf_text)
        
        # Store the text in the knowledge base
        knowledge_base[file.filename] = full_text
        
        return {"filename": file.filename, "message": "PDF uploaded and text extracted successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def get_answer(query: Query):
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="No PDF uploaded.")
    
    # Simulate querying the knowledge base (you can implement RAG here)
    for filename, text in knowledge_base.items():
        if query.query.lower() in text.lower():
            return {"answer": f"Found in {filename}: {text[:100]}..."}  # Returning first 100 characters

    return {"answer": "No relevant information found."}
