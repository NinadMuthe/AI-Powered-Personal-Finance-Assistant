from fastapi import FastAPI
from backend.app.api import api_router
from backend.app.api.routes import router

app = FastAPI(
    title="AI-Powered Personal Finance Assistant",
    description="Backend API for an AI-powered personal finance assistant.",
    version="1.0.0"
)

api_router.include_router(router)
app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "AI-Powered Personal Finance Assistant API is running"
    }