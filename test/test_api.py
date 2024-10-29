# tests/test_api.py
import unittest
from fastapi.testclient import TestClient
from backend.api import app  # Assuming you're using FastAPI

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # tests/test_api.py
def test_query_endpoint_with_valid_query(self):
    response = self.client.post("/query", json={"question": "What is AI?"})
    self.assertEqual(response.status_code, 200)
    self.assertIn("answer", response.json(), "Response should contain an answer field")


    def test_query_endpoint_missing_query(self):
        response = self.client.post("/query", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json(), "Response should contain an error field for bad requests")
