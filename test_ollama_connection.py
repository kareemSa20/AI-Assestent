import httpx
import asyncio
import os

OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen2.5:7b"

async def test_connection():
    print(f"[TEST] Testing connection to {OLLAMA_URL}...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            print(f"[OK] Service Status: {resp.status_code}")
            if resp.status_code == 200:
                models = [m['name'] for m in resp.json().get('models', [])]
                print(f"[INFO] Available Models: {models}")
                if MODEL in models:
                    print(f"[OK] Model '{MODEL}' found!")
                else:
                    print(f"[FAIL] Model '{MODEL}' NOT found in list. Found: {models}")
            else:
                print(f"[FAIL] Service returned error: {resp.text}")

        print(f"\n[TEST] Testing Inference with '{MODEL}' (Timeout 60s)...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": "hello"}],
                "stream": False
            }
            resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            if resp.status_code == 200:
                 print(f"[SUCCESS] Inference Success: {resp.json()['message']['content'][:50]}...")
            else:
                 print(f"[FAIL] Inference Failed: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[ERROR] Connection Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
