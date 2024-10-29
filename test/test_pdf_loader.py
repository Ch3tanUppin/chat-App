# test/test_pdf_loader.py
import unittest
from unittest.mock import MagicMock
from fastapi import UploadFile
from backend.pdf_loader import load_pdf

class TestPDFLoader(unittest.TestCase):

    async def test_load_pdf_success(self):
        # Create a mock PDF file with some content
        mock_pdf_content = b'%PDF-1.4\n%.... (some valid PDF content)'
        empty_mock_file = UploadFile(filename="test.pdf", content_type="application/pdf", file=MagicMock())
        empty_mock_file.file.read = MagicMock(return_value=mock_pdf_content)
        
        # Await the load_pdf method
        content = await load_pdf(empty_mock_file)
        self.assertIsInstance(content, str)

    async def test_load_pdf_empty(self):
        # Create an empty mock PDF file
        empty_mock_file = UploadFile(filename="empty.pdf", content_type="application/pdf", file=MagicMock())
        empty_mock_file.file.read = MagicMock(return_value=b'')  # No content

        with self.assertRaises(ValueError) as context:
            await load_pdf(empty_mock_file)  # Await the function
        self.assertEqual(str(context.exception), "No text found in the PDF.")
