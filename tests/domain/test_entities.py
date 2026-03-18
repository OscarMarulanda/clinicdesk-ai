"""Unit tests for domain entities."""

from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.article import Article, ArticleCategory, ArticleSearchResult
from src.domain.entities.escalation import Escalation, EscalationReason, EscalationStatus
from src.domain.entities.provider import Provider
from src.domain.entities.session import Message, Session, SessionStatus
from src.domain.entities.user import User, UserRole


class TestUser:
    def test_create_user(self):
        user = User(
            id=1, email="test@example.com", name="Test User",
            role=UserRole.STAFF, password_hash="hash",
            created_at=datetime.now(timezone.utc),
        )
        assert user.email == "test@example.com"
        assert user.role == UserRole.STAFF
        assert not user.is_admin

    def test_admin_role(self):
        user = User(
            id=1, email="admin@example.com", name="Admin",
            role=UserRole.ADMIN, password_hash="hash",
            created_at=datetime.now(timezone.utc),
        )
        assert user.is_admin

    def test_user_role_enum(self):
        assert UserRole.STAFF.value == "staff"
        assert UserRole.ADMIN.value == "admin"


class TestArticle:
    def test_create_article(self):
        article = Article(
            id=1, title="Test Article", slug="test-article",
            category=ArticleCategory.SCHEDULING, content="Content here",
            created_by=1, updated_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
        )
        assert article.title == "Test Article"
        assert article.category == ArticleCategory.SCHEDULING

    def test_article_categories(self):
        assert len(ArticleCategory) == 7
        assert ArticleCategory.BILLING_CODING.value == "billing_coding"
        assert ArticleCategory.INSURANCE_CLAIMS.value == "insurance_claims"

    def test_search_result(self):
        result = ArticleSearchResult(
            id=1, title="Test", category=ArticleCategory.SCHEDULING,
            content="Content", rank=0.95,
        )
        assert result.rank == 0.95


class TestSession:
    def test_create_session(self):
        session = Session(
            id=uuid4(), user_id=1, channel="chat",
            status=SessionStatus.ACTIVE, context={}, messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        assert session.status == SessionStatus.ACTIVE
        assert len(session.messages) == 0

    def test_add_message(self):
        session = Session(
            id=uuid4(), user_id=None, channel="chat",
            status=SessionStatus.ACTIVE, context={}, messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        msg = Message(role="user", content="Hello", timestamp=datetime.now(timezone.utc))
        session.add_message(msg)
        assert len(session.messages) == 1
        assert session.messages[0].content == "Hello"

    def test_update_context(self):
        session = Session(
            id=uuid4(), user_id=None, channel="chat",
            status=SessionStatus.ACTIVE, context={}, messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.update_context("notes", "Resolved issue")
        assert session.context["notes"] == "Resolved issue"

    def test_close_session(self):
        session = Session(
            id=uuid4(), user_id=None, channel="chat",
            status=SessionStatus.ACTIVE, context={}, messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.close()
        assert session.status == SessionStatus.CLOSED


class TestEscalation:
    def test_create_escalation(self):
        esc = Escalation(
            id=1, session_id=uuid4(), reason=EscalationReason.BILLING_DISPUTE,
            summary="Double charge", status=EscalationStatus.PENDING,
            assigned_to="support@test.com", calendar_event_id=None,
            email_sent_at=None, created_at=datetime.now(timezone.utc),
            resolved_at=None,
        )
        assert esc.reason == EscalationReason.BILLING_DISPUTE
        assert esc.status == EscalationStatus.PENDING

    def test_escalation_reasons(self):
        assert len(EscalationReason) == 5

    def test_escalation_statuses(self):
        assert EscalationStatus.PENDING.value == "pending"
        assert EscalationStatus.IN_PROGRESS.value == "in_progress"
        assert EscalationStatus.RESOLVED.value == "resolved"


class TestProvider:
    def test_create_provider(self):
        provider = Provider(
            id=1, name="Dr. Smith", email="smith@clinic.com",
            calendar_id="smith@clinic.com", is_available=True,
            created_at=datetime.now(timezone.utc),
        )
        assert provider.is_available
        assert provider.name == "Dr. Smith"
