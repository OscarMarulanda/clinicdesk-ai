"""Shared test fixtures."""

import asyncpg
import pytest_asyncio

from src.infrastructure.ai.claude_service import ClaudeAIService
from src.infrastructure.calendar.google_calendar_service import GoogleCalendarService
from src.infrastructure.email.sendgrid_service import SendGridEmailService
from src.main import app

TEST_DB = "postgresql://localhost:5432/clinicdesk"


@pytest_asyncio.fixture(scope="session")
async def pool():
    """Shared connection pool for all tests."""
    p = await asyncpg.create_pool(dsn=TEST_DB, min_size=1, max_size=5)
    app.state.db_pool = p
    app.state.ai_service = ClaudeAIService()
    app.state.calendar_service = GoogleCalendarService()
    app.state.email_service = SendGridEmailService()
    yield p
    await p.close()
