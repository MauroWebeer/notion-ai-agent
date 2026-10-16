from fastapi import FastAPI
from src.config import settings

app = FastAPI(
    title="Notion AI Agent API",
    description="API REST integrando FastAPI, LangChain, Groq, Notion e LangFuse",
    version="0.1.0",
)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "app": "Notion AI Agent",
        "debug_mode": settings.DEBUG,
    }