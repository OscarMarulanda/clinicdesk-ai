class DomainException(Exception):
    """Base exception for domain errors."""


class EntityNotFoundError(DomainException):
    def __init__(self, entity_type: str, identifier: object) -> None:
        self.entity_type = entity_type
        self.identifier = identifier
        super().__init__(f"{entity_type} not found: {identifier}")


class DuplicateEntityError(DomainException):
    def __init__(self, entity_type: str, field: str, value: object) -> None:
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field}={value} already exists")


class AuthenticationError(DomainException):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message)


class AuthorizationError(DomainException):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message)
