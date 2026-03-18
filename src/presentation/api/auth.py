from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.exceptions import AuthenticationError
from src.presentation.dependencies import get_auth_use_case

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    auth_use_case: AuthenticateUserUseCase = Depends(get_auth_use_case),
):
    try:
        token, user = await auth_use_case.login(request.email, request.password)
        return LoginResponse(
            token=token,
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value,
            },
        )
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
