from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.models import User
from app.modules.users.schemas import UserMeResponse


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    token = AuthService(db).login(
        email=payload.email,
        password=payload.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserMeResponse)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user