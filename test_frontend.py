from fastapi.testclient import TestClient
import sys
import os

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
sys.path.append(os.path.dirname(__file__))

from app.main import app

client = TestClient(app)

def test_static_serving():
    print("Testing Static File Serving...")
    
    # 1. Test Root
    resp = client.get("/")
    print(f"Root Status: {resp.status_code}")
    assert resp.status_code == 200
    assert "<!DOCTYPE html>" in resp.text
    print("✅ Root Index Served")

    # 2. Test JS
    resp = client.get("/static/js/app.js")
    print(f"JS Status: {resp.status_code}")
    assert resp.status_code == 200
    assert "const API_BASE" in resp.text
    print("✅ JS Asset Served")
    
    print("Frontend Verification Passed!")

if __name__ == "__main__":
    test_static_serving()
