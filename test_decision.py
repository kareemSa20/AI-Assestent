from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime

# Setup path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
sys.path.append(os.path.dirname(__file__))

from app.main import app

client = TestClient(app)

def test_decision_engine():
    print("Testing Decision Engine...")
    
    # Scene 1: Hard Rule Trigger (Critical Defect)
    print("\n--- Test 1: Critical Defect (Hard Rule) ---")
    event_critical = {
        "event_id": "TEST-001",
        "timestamp": "2023-01-01",
        "event_type": "Damage",
        "details": "GlassBroken inside pallet",
        "severity": "Critical"
    }
    resp = client.post("/api/v1/analyze/event", json=event_critical)
    print(f"Response: {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()['source'] == "HardRule_SafetyProtocol_v1"
    assert resp.json()['action'] == "IMMEDIATE_DISPOSAL"
    print("Hard Rule Passed")

    # Scene 2: AI Trigger (Ambiguous Damaged Box)
    print("\n--- Test 2: Ambiguous Damage (AI Reasoning) ---")
    event_ambiguous = {
        "event_id": "TEST-002",
        "timestamp": "2023-01-01",
        "event_type": "Damage",
        "details": "Minor dent on side of box",
        "severity": "Low"
    }
    resp = client.post("/api/v1/analyze/event", json=event_ambiguous)
    # Note: Since LLM is Mocked, we expect the Mock Response
    print(f"Response: {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()['source'] == "AI_LLM_Reasoning"
    print("AI Logic Passed")

if __name__ == "__main__":
    test_decision_engine()
