# tests/test_rag_retrieval.py
import unittest
from unittest.mock import patch, Mock

import requests
from backend.rag_retrieval import RAG

class TestRAG(unittest.TestCase):

    def setUp(self):
        self.knowledge_base = "sample_knowledge_base"
        self.api_key = "test_api_key"
        self.rag = RAG(self.knowledge_base, self.api_key)

    @patch('backend.rag_retrieval.requests.post')
    def test_generate_answer_success(self, mock_post):
        # Mock response from the Gemini API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"answer": "This is the answer."}
        mock_post.return_value = mock_response
        
        # Call the method under test
        answer = self.rag.generate_answer("What is AI?")
        self.assertEqual(answer, "This is the answer.")

    @patch('backend.rag_retrieval.requests.post')
    def test_generate_answer_http_error(self, mock_post):
        # Mock response to raise an HTTP error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post.return_value = mock_response
        
        with self.assertRaises(Exception) as context:
            self.rag.generate_answer("What is AI?")
        self.assertIn("Error: 404, Not Found", str(context.exception))

        # tests/test_rag_retrieval.py
@patch('backend.rag_retrieval.requests.post')
def test_generate_answer_request_exception(self, mock_post):
    # Mock request to raise a connection error
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection error")
    
    with self.assertRaises(Exception) as context:
        self.rag.generate_answer("What is AI?")
    # Adjust the message check to match the exact message from the exception
    self.assertEqual(str(context.exception), "Request error occurred: Connection error")


    @patch('backend.rag_retrieval.requests.post')
    def test_generate_answer_request_exception(self, mock_post):
        # Mock request to raise a connection error
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection error")
        
        with self.assertRaises(Exception) as context:
            self.rag.generate_answer("What is AI?")
        self.assertIn("Request error occurred: Connection error", str(context.exception))

