"""FastAPI application entry point for the Study AI Assistant Helper."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from study_ai_assistant_helper.app.config.settings import fast_api_base_settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=fast_api_base_settings.FAST_API_SECRET_KEY)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    """Return the API health status."""
    return {"status": "API is up and running and healthy!"}