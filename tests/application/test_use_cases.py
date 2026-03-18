"""Unit tests for application use cases with mocked repositories."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.domain.entities.article import Article, ArticleCategory, ArticleSearchResult
from src.domain.entities.escalation import Escalation, EscalationReason, EscalationStatus
from src.domain.entities.session import Session, SessionStatus
from src.domain.entities.user import User, UserRole
from src.domain.exceptions import EntityNotFoundError


class TestSearchKnowledgeBase:
    @pytest.mark.asyncio
    async def test_search_returns_results(self):
        from src.application.use_cases.search_knowledge_base import SearchKnowledgeBaseUseCase

        mock_repo = AsyncMock()
        mock_repo.search.return_value = [
            ArticleSearchResult(id=1, title="Test", category=ArticleCategory.SCHEDULING, content="Content", rank=0.9),
        ]
        use_case = SearchKnowledgeBaseUseCase(mock_repo)
        results = await use_case.execute("appointment")
        assert len(results) == 1
        assert results[0].rank == 0.9
        mock_repo.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_category(self):
        from src.application.use_cases.search_knowledge_base import SearchKnowledgeBaseUseCase

        mock_repo = AsyncMock()
        mock_repo.search.return_value = []
        use_case = SearchKnowledgeBaseUseCase(mock_repo)
        await use_case.execute("test", category="scheduling")
        mock_repo.search.assert_called_once_with("test", category=ArticleCategory.SCHEDULING, limit=5)

    @pytest.mark.asyncio
    async def test_search_empty(self):
        from src.application.use_cases.search_knowledge_base import SearchKnowledgeBaseUseCase

        mock_repo = AsyncMock()
        mock_repo.search.return_value = []
        use_case = SearchKnowledgeBaseUseCase(mock_repo)
        results = await use_case.execute("nonexistent")
        assert len(results) == 0


class TestGetArticle:
    @pytest.mark.asyncio
    async def test_get_existing_article(self):
        from src.application.use_cases.get_article import GetArticleUseCase

        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = Article(
            id=1, title="Test", slug="test", category=ArticleCategory.SCHEDULING,
            content="Content", created_by=None,
            updated_at=datetime.now(timezone.utc), created_at=datetime.now(timezone.utc),
        )
        use_case = GetArticleUseCase(mock_repo)
        article = await use_case.execute(1)
        assert article.title == "Test"

    @pytest.mark.asyncio
    async def test_get_nonexistent_article(self):
        from src.application.use_cases.get_article import GetArticleUseCase

        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        use_case = GetArticleUseCase(mock_repo)
        with pytest.raises(EntityNotFoundError):
            await use_case.execute(999)


class TestManageArticles:
    @pytest.mark.asyncio
    async def test_create_article(self):
        from src.application.use_cases.manage_articles import ManageArticlesUseCase

        mock_repo = AsyncMock()
        mock_repo.create.return_value = Article(
            id=1, title="New Article", slug="new-article",
            category=ArticleCategory.BILLING_CODING, content="Content",
            created_by=1, updated_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
        )
        use_case = ManageArticlesUseCase(mock_repo)
        article = await use_case.create_article("New Article", "billing_coding", "Content", created_by=1)
        assert article.title == "New Article"
        mock_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self):
        from src.application.use_cases.manage_articles import ManageArticlesUseCase

        mock_repo = AsyncMock()
        mock_repo.delete.return_value = False
        use_case = ManageArticlesUseCase(mock_repo)
        with pytest.raises(EntityNotFoundError):
            await use_case.delete_article(999)

    @pytest.mark.asyncio
    async def test_list_articles(self):
        from src.application.use_cases.manage_articles import ManageArticlesUseCase

        mock_repo = AsyncMock()
        mock_repo.list_all.return_value = ([], 0)
        use_case = ManageArticlesUseCase(mock_repo)
        articles, total = await use_case.list_articles()
        assert total == 0
        assert articles == []


class TestGetSessions:
    @pytest.mark.asyncio
    async def test_list_sessions(self):
        from src.application.use_cases.get_sessions import GetSessionsUseCase

        mock_repo = AsyncMock()
        mock_repo.list_all.return_value = ([], 0)
        use_case = GetSessionsUseCase(mock_repo)
        sessions, total = await use_case.list_all()
        assert total == 0

    @pytest.mark.asyncio
    async def test_get_nonexistent_session(self):
        from src.application.use_cases.get_sessions import GetSessionsUseCase

        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        use_case = GetSessionsUseCase(mock_repo)
        with pytest.raises(EntityNotFoundError):
            await use_case.get_detail(uuid4())


class TestManageEscalations:
    @pytest.mark.asyncio
    async def test_update_status(self):
        from src.application.use_cases.manage_escalations import ManageEscalationsUseCase

        mock_repo = AsyncMock()
        mock_repo.update_status.return_value = Escalation(
            id=1, session_id=uuid4(), reason=EscalationReason.BILLING_DISPUTE,
            summary="Test", status=EscalationStatus.RESOLVED,
            assigned_to=None, calendar_event_id=None, email_sent_at=None,
            created_at=datetime.now(timezone.utc), resolved_at=datetime.now(timezone.utc),
        )
        use_case = ManageEscalationsUseCase(mock_repo)
        esc = await use_case.update_status(1, "resolved")
        assert esc.status == EscalationStatus.RESOLVED

    @pytest.mark.asyncio
    async def test_update_nonexistent(self):
        from src.application.use_cases.manage_escalations import ManageEscalationsUseCase

        mock_repo = AsyncMock()
        mock_repo.update_status.return_value = None
        use_case = ManageEscalationsUseCase(mock_repo)
        with pytest.raises(EntityNotFoundError):
            await use_case.update_status(999, "resolved")


class TestListCategories:
    @pytest.mark.asyncio
    async def test_list_categories(self):
        from src.application.use_cases.list_categories import ListCategoriesUseCase

        mock_repo = AsyncMock()
        mock_repo.list_categories.return_value = ["scheduling", "billing_coding"]
        use_case = ListCategoriesUseCase(mock_repo)
        cats = await use_case.execute()
        assert len(cats) == 2
        assert "scheduling" in cats


class TestUpdateSessionNotes:
    @pytest.mark.asyncio
    async def test_update_notes(self):
        from src.application.use_cases.update_session_notes import UpdateSessionNotesUseCase

        session_id = uuid4()
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = Session(
            id=session_id, user_id=None, channel="chat",
            status=SessionStatus.ACTIVE, context={}, messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        use_case = UpdateSessionNotesUseCase(mock_repo)
        await use_case.execute(session_id, "Test notes")
        mock_repo.update_context.assert_called_once()
        call_args = mock_repo.update_context.call_args
        assert call_args[0][1]["notes"] == "Test notes"

    @pytest.mark.asyncio
    async def test_update_notes_nonexistent_session(self):
        from src.application.use_cases.update_session_notes import UpdateSessionNotesUseCase

        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        use_case = UpdateSessionNotesUseCase(mock_repo)
        with pytest.raises(EntityNotFoundError):
            await use_case.execute(uuid4(), "Notes")
