# backend/pdf_loader.py
from PyPDF2 import PdfReader
from fastapi import UploadFile
from io import BytesIO

async def load_pdf(uploaded_file: UploadFile):
    text = ""
    contents = await uploaded_file.read()  # Read the content of the uploaded file
    pdf_reader = PdfReader(BytesIO(contents))  # Use BytesIO to create a file-like object

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:  # Check if text extraction is successful
            text += page_text

    if not text.strip():  # Raise an error if no text was extracted
        raise ValueError("No text found in the PDF.")
    return text
