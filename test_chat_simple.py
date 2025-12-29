from fastapi.testclient import TestClient
import sys
import os

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
sys.path.append(os.path.dirname(__file__))

from app.main import app

client = TestClient(app)

def test_chat_api():
    print("Testing Chat API...")
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello, is the system running?", "context": {"user_id": "123"}}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "retrieved_context" in response.json()
    print("Chat API Test Passed! ✅")

if __name__ == "__main__":
    test_chat_api()
