"""Shared SQLModel metadata used by Alembic migrations."""

from sqlmodel import SQLModel

from study_ai_assistant_helper.app.db import models


metadata = SQLModel.metadata

__all__ = ["metadata"]