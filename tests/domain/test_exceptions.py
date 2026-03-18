"""Unit tests for domain exceptions."""

from src.domain.exceptions import (
    AuthenticationError,
    AuthorizationError,
    DomainException,
    DuplicateEntityError,
    EntityNotFoundError,
)


class TestExceptions:
    def test_entity_not_found(self):
        exc = EntityNotFoundError("Article", 42)
        assert "Article" in str(exc)
        assert "42" in str(exc)
        assert exc.entity_type == "Article"
        assert exc.identifier == 42

    def test_duplicate_entity(self):
        exc = DuplicateEntityError("User", "email", "test@test.com")
        assert "User" in str(exc)
        assert "email" in str(exc)
        assert exc.field == "email"

    def test_authentication_error(self):
        exc = AuthenticationError()
        assert "Invalid credentials" in str(exc)

    def test_authentication_error_custom_message(self):
        exc = AuthenticationError("Token expired")
        assert "Token expired" in str(exc)

    def test_authorization_error(self):
        exc = AuthorizationError()
        assert "Insufficient permissions" in str(exc)

    def test_inheritance(self):
        assert issubclass(EntityNotFoundError, DomainException)
        assert issubclass(DuplicateEntityError, DomainException)
        assert issubclass(AuthenticationError, DomainException)
        assert issubclass(AuthorizationError, DomainException)
