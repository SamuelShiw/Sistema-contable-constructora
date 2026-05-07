from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.roles.models import Role
from app.modules.users.models import User
from app.modules.users.user_roles import UserRole


def get_user_roles(
    user_id: int,
    db: Session,
) -> list[str]:
    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )

    return [row[0] for row in rows]


def require_roles(
    allowed_roles: list[str],
) -> Callable:
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        user_roles = get_user_roles(
            user_id=current_user.id,
            db=db,
        )

        if "ADMIN" in user_roles:
            return current_user

        has_access = any(role in allowed_roles for role in user_roles)

        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )

        return current_user

    return dependency