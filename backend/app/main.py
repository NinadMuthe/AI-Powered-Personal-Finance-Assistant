from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Personal Finance Assistant",
    description="Backend API for an AI-powered personal finance assistant.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI-Powered Personal Finance Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }