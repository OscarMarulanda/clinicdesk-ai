import bcrypt
import jwt
from datetime import datetime, timezone, timedelta

from src.domain.entities.user import User
from src.domain.exceptions import AuthenticationError
from src.domain.repositories.user_repository import UserRepositoryBase
from src.infrastructure.config import settings


class AuthenticateUserUseCase:
    def __init__(self, user_repo: UserRepositoryBase) -> None:
        self._user_repo = user_repo

    async def login(self, email: str, password: str) -> tuple[str, User]:
        """Authenticate and return (token, user)."""
        user = await self._user_repo.get_by_email(email)
        if user is None:
            raise AuthenticationError()

        if not bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            raise AuthenticationError()

        token = self._create_token(user)
        return token, user

    def verify_token(self, token: str) -> dict:
        """Verify a JWT token and return the payload."""
        try:
            payload = jwt.decode(
                token, settings.app_secret_key, algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

    @staticmethod
    def _create_token(user: User) -> str:
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }
        return jwt.encode(payload, settings.app_secret_key, algorithm="HS256")
