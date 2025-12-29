from fastapi.testclient import TestClient
import sys
import os

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
sys.path.append(os.path.dirname(__file__))

from app.main import app

client = TestClient(app)

def test_integration_endpoints():
    print("Testing System Integration API...")
    
    # 1. Test Status
    resp = client.get("/api/v1/system/status")
    print(f"Status: {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()['vision_system_active'] == True

    # 2. Test Stock
    resp = client.get("/api/v1/system/stock")
    print(f"Stock: {resp.json()}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    assert "Saudi Milk" in str(resp.json())

    # 3. Test Events
    resp = client.get("/api/v1/system/events")
    print(f"Events: {resp.json()}")
    assert resp.status_code == 200
    assert "DamagedBox" in str(resp.json())

    print("Integration Tests Passed! ✅")

if __name__ == "__main__":
    test_integration_endpoints()
