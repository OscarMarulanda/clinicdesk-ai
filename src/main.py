import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.infrastructure.ai.claude_service import ClaudeAIService
from src.infrastructure.calendar.google_calendar_service import GoogleCalendarService
from src.infrastructure.database.connection import close_pool, get_pool
from src.infrastructure.email.sendgrid_service import SendGridEmailService
from src.presentation.api.analytics import router as analytics_router
from src.presentation.api.articles import router as articles_router
from src.presentation.api.auth import router as auth_router
from src.presentation.api.escalations import router as escalations_router
from src.presentation.api.notifications import router as notifications_router
from src.presentation.api.sessions import router as sessions_router
from src.presentation.ws.admin import router as admin_ws_router
from src.presentation.ws.chat import router as chat_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — wire infrastructure services
    pool = await get_pool()
    app.state.db_pool = pool
    app.state.ai_service = ClaudeAIService()
    app.state.calendar_service = GoogleCalendarService()
    app.state.email_service = SendGridEmailService()
    yield
    # Shutdown
    await close_pool()


app = FastAPI(
    title="ClinicDesk AI",
    description="AI-powered customer support agent for practice management software",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(admin_ws_router)
app.include_router(articles_router)
app.include_router(sessions_router)
app.include_router(escalations_router)
app.include_router(notifications_router)
app.include_router(analytics_router)

# Static files for frontend
app.mount("/static/widget", StaticFiles(directory="frontend/widget"), name="widget")
app.mount("/static/admin", StaticFiles(directory="frontend/admin"), name="admin")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
