from fastapi import Depends, Request

import asyncpg

from src.application.interfaces.ai_service import AIServiceInterface
from src.application.interfaces.calendar_service import CalendarServiceInterface
from src.application.interfaces.email_service import EmailServiceInterface
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.use_cases.get_analytics import GetAnalyticsUseCase
from src.application.use_cases.get_sessions import GetSessionsUseCase
from src.application.use_cases.manage_articles import ManageArticlesUseCase
from src.application.use_cases.manage_escalations import ManageEscalationsUseCase
from src.application.use_cases.process_chat_message import ProcessChatMessageUseCase
from src.infrastructure.database.escalation_repository import PostgresEscalationRepository
from src.infrastructure.database.knowledge_repository import PostgresKnowledgeRepository
from src.infrastructure.database.session_repository import PostgresSessionRepository
from src.infrastructure.database.user_repository import PostgresUserRepository


def get_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool


def get_ai_service(request: Request) -> AIServiceInterface:
    return request.app.state.ai_service


def get_calendar_service(request: Request) -> CalendarServiceInterface:
    return request.app.state.calendar_service


def get_email_service(request: Request) -> EmailServiceInterface:
    return request.app.state.email_service


def get_process_chat_use_case(
    pool: asyncpg.Pool = Depends(get_pool),
    ai_service: AIServiceInterface = Depends(get_ai_service),
    calendar_service: CalendarServiceInterface = Depends(get_calendar_service),
    email_service: EmailServiceInterface = Depends(get_email_service),
) -> ProcessChatMessageUseCase:
    return ProcessChatMessageUseCase(
        ai_service=ai_service,
        session_repo=PostgresSessionRepository(pool),
        knowledge_repo=PostgresKnowledgeRepository(pool),
        escalation_repo=PostgresEscalationRepository(pool),
        user_repo=PostgresUserRepository(pool),
        calendar_service=calendar_service,
        email_service=email_service,
    )


def get_manage_articles_use_case(
    pool: asyncpg.Pool = Depends(get_pool),
) -> ManageArticlesUseCase:
    return ManageArticlesUseCase(PostgresKnowledgeRepository(pool))


def get_sessions_use_case(
    pool: asyncpg.Pool = Depends(get_pool),
) -> GetSessionsUseCase:
    return GetSessionsUseCase(PostgresSessionRepository(pool))


def get_manage_escalations_use_case(
    pool: asyncpg.Pool = Depends(get_pool),
) -> ManageEscalationsUseCase:
    return ManageEscalationsUseCase(PostgresEscalationRepository(pool))


def get_analytics_use_case(
    pool: asyncpg.Pool = Depends(get_pool),
) -> GetAnalyticsUseCase:
    return GetAnalyticsUseCase(pool)


def get_auth_use_case(
    pool: asyncpg.Pool = Depends(get_pool),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(PostgresUserRepository(pool))
