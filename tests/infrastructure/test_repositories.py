"""Integration tests for PostgreSQL repositories — runs against real database."""

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.domain.entities.article import ArticleCategory
from src.domain.entities.escalation import EscalationStatus
from src.domain.entities.session import SessionStatus
from src.domain.entities.user import UserRole
from src.infrastructure.database.escalation_repository import PostgresEscalationRepository
from src.infrastructure.database.knowledge_repository import PostgresKnowledgeRepository
from src.infrastructure.database.provider_repository import PostgresProviderRepository
from src.infrastructure.database.session_repository import PostgresSessionRepository
from src.infrastructure.database.user_repository import PostgresUserRepository


class TestKnowledgeRepository:
    @pytest.mark.asyncio
    async def test_search_finds_articles(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        results = await repo.search("appointment")
        assert len(results) > 0
        assert results[0].rank > 0

    @pytest.mark.asyncio
    async def test_search_with_category_filter(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        results = await repo.search("appointment", category=ArticleCategory.SCHEDULING)
        for r in results:
            assert r.category == ArticleCategory.SCHEDULING

    @pytest.mark.asyncio
    async def test_search_no_results(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        results = await repo.search("xyznonexistent12345")
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_create_and_get(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        slug = f"test-article-{uuid4().hex[:8]}"
        article = await repo.create(
            title="Test Article", slug=slug,
            category=ArticleCategory.SCHEDULING,
            content="Test content for search",
        )
        assert article.id is not None
        fetched = await repo.get_by_id(article.id)
        assert fetched is not None
        assert fetched.slug == slug
        await repo.delete(article.id)

    @pytest.mark.asyncio
    async def test_update_article(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        slug = f"test-update-{uuid4().hex[:8]}"
        article = await repo.create(
            title="Original", slug=slug,
            category=ArticleCategory.SCHEDULING, content="Original content",
        )
        updated = await repo.update(article.id, title="Updated Title")
        assert updated.title == "Updated Title"
        await repo.delete(article.id)

    @pytest.mark.asyncio
    async def test_list_all(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        articles, total = await repo.list_all()
        assert total >= 67
        assert len(articles) > 0

    @pytest.mark.asyncio
    async def test_list_categories(self, pool):
        repo = PostgresKnowledgeRepository(pool)
        cats = await repo.list_categories()
        assert "scheduling" in cats
        assert len(cats) == 7

    def test_generate_slug(self):
        assert PostgresKnowledgeRepository.generate_slug("How to Book an Appointment") == "how-to-book-an-appointment"


class TestSessionRepository:
    @pytest.mark.asyncio
    async def test_create_session(self, pool):
        repo = PostgresSessionRepository(pool)
        session = await repo.create()
        assert session.id is not None
        assert session.status == SessionStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_get_session(self, pool):
        repo = PostgresSessionRepository(pool)
        session = await repo.create()
        fetched = await repo.get_by_id(session.id)
        assert fetched is not None
        assert fetched.id == session.id

    @pytest.mark.asyncio
    async def test_update_messages(self, pool):
        repo = PostgresSessionRepository(pool)
        session = await repo.create()
        messages = [
            {"role": "user", "content": "Hello", "timestamp": datetime.now(timezone.utc).isoformat()},
            {"role": "assistant", "content": "Hi!", "timestamp": datetime.now(timezone.utc).isoformat()},
        ]
        await repo.update_messages(session.id, messages)
        fetched = await repo.get_by_id(session.id)
        assert len(fetched.messages) == 2

    @pytest.mark.asyncio
    async def test_update_context(self, pool):
        repo = PostgresSessionRepository(pool)
        session = await repo.create()
        await repo.update_context(session.id, {"notes": "Test note"})
        fetched = await repo.get_by_id(session.id)
        assert fetched.context["notes"] == "Test note"

    @pytest.mark.asyncio
    async def test_update_status(self, pool):
        repo = PostgresSessionRepository(pool)
        session = await repo.create()
        await repo.update_status(session.id, SessionStatus.CLOSED)
        fetched = await repo.get_by_id(session.id)
        assert fetched.status == SessionStatus.CLOSED

    @pytest.mark.asyncio
    async def test_list_all(self, pool):
        repo = PostgresSessionRepository(pool)
        sessions, total = await repo.list_all()
        assert total >= 1


class TestEscalationRepository:
    @pytest.mark.asyncio
    async def test_create_escalation(self, pool):
        session_repo = PostgresSessionRepository(pool)
        session = await session_repo.create()
        repo = PostgresEscalationRepository(pool)
        esc = await repo.create(
            session_id=session.id, reason="billing_dispute",
            summary="Test escalation", assigned_to="test@test.com",
        )
        assert esc.id is not None
        assert esc.status == EscalationStatus.PENDING

    @pytest.mark.asyncio
    async def test_update_escalation_status(self, pool):
        session_repo = PostgresSessionRepository(pool)
        session = await session_repo.create()
        repo = PostgresEscalationRepository(pool)
        esc = await repo.create(
            session_id=session.id, reason="knowledge_gap",
            summary="Test", assigned_to="test@test.com",
        )
        updated = await repo.update_status(esc.id, EscalationStatus.RESOLVED)
        assert updated.status == EscalationStatus.RESOLVED
        assert updated.resolved_at is not None

    @pytest.mark.asyncio
    async def test_set_calendar_event(self, pool):
        session_repo = PostgresSessionRepository(pool)
        session = await session_repo.create()
        repo = PostgresEscalationRepository(pool)
        esc = await repo.create(session_id=session.id, reason="billing_dispute", summary="Test")
        await repo.set_calendar_event(esc.id, "event-123")
        fetched = await repo.get_by_id(esc.id)
        assert fetched.calendar_event_id == "event-123"


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_get_by_email(self, pool):
        repo = PostgresUserRepository(pool)
        user = await repo.get_by_email("admin@clinicdesk.com")
        assert user is not None
        assert user.role == UserRole.ADMIN

    @pytest.mark.asyncio
    async def test_get_nonexistent(self, pool):
        repo = PostgresUserRepository(pool)
        user = await repo.get_by_email("nonexistent@example.com")
        assert user is None

    @pytest.mark.asyncio
    async def test_list_all(self, pool):
        repo = PostgresUserRepository(pool)
        users = await repo.list_all()
        assert len(users) >= 3


class TestProviderRepository:
    @pytest.mark.asyncio
    async def test_get_available(self, pool):
        repo = PostgresProviderRepository(pool)
        providers = await repo.get_available()
        assert len(providers) >= 2
        for p in providers:
            assert p.is_available

    @pytest.mark.asyncio
    async def test_list_all(self, pool):
        repo = PostgresProviderRepository(pool)
        providers = await repo.list_all()
        assert len(providers) >= 3
