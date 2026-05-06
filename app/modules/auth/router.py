from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.audit.service import AuditLogService
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
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    service = AuthService(db)

    token = service.login(
        email=payload.email,
        password=payload.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    user = service.get_user_by_email(payload.email)

    AuditLogService(db).register(
        action="LOGIN",
        module="AUTH",
        table_name="users",
        record_id=user.id if user else None,
        user_id=user.id if user else None,
        ip_address=request.client.host if request.client else None,
    )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserMeResponse)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user