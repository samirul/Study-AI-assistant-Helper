"""FastAPI application entry point for the Study AI Assistant Helper."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from study_ai_assistant_helper.app.config.settings import fast_api_base_settings
from study_ai_assistant_helper.app.db.session import async_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Release pooled database connections when the application shuts down."""
    try:
        yield
    finally:
        await async_engine.dispose()


app = FastAPI(lifespan=lifespan)
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