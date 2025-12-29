import sys
import os

# Add the project root to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "app"))
# Add the ai_core root
sys.path.append(current_dir)

try:
    print("Attempting to import FastAPI app...")
    from app.main import app
    from app.core.settings import settings
    
    print(f"Successfully imported app: {settings.PROJECT_NAME}")
    print("Verifying vector store initialization (mock)...")
    
    # We won't actually init vector store as it might create files, 
    # but we can check if the class is importable.
    from app.memory.vector_store import VectorStore
    print("VectorStore class imported successfully.")
    
    print("Verifying LLM Client...")
    from app.services.llm_client import LLMClient
    print("LLMClient class imported successfully.")
    
    print("ALL CHECKS PASSED.")
except Exception as e:
    print(f"VERIFICATION FAILED: {e}")
    import traceback
    traceback.print_exc()
