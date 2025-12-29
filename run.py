import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Nasseh AI System on Port 8005...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8005, reload=True)
