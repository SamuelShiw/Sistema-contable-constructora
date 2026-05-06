from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.modules.users.models import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def login(self, email: str, password: str) -> str | None:
        user = (
            self.db.query(User)
            .filter(User.email == email, User.is_active.is_(True))
            .first()
        )

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return create_access_token(subject=str(user.id))