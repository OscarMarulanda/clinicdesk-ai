from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.exceptions import AuthenticationError
from src.presentation.dependencies import get_auth_use_case

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_use_case: AuthenticateUserUseCase = Depends(get_auth_use_case),
) -> dict:
    try:
        payload = auth_use_case.verify_token(credentials.credentials)
        return payload
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def require_admin(
    current_user: dict = Depends(get_current_user),
) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
