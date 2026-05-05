from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.modules.companies.models import Company
from app.modules.roles.models import Role
from app.modules.users.models import User
from app.modules.users.user_roles import UserRole


def seed_admin() -> None:
    db: Session = SessionLocal()

    try:
        company = db.query(Company).filter(Company.ruc == "20600000001").first()

        if company is None:
            company = Company(
                business_name="Constructora Demo S.A.C.",
                ruc="20600000001",
                address="Av. Principal 123",
                phone="999999999",
                email="contacto@constructorademo.com",
                legal_representative="Administrador General",
                currency="PEN",
            )
            db.add(company)
            db.commit()
            db.refresh(company)

        role = db.query(Role).filter(Role.name == "ADMIN").first()

        if role is None:
            role = Role(
                name="ADMIN",
                description="Administrador general del sistema",
            )
            db.add(role)
            db.commit()
            db.refresh(role)

        user = db.query(User).filter(User.email == "admin@constructora.com").first()

        if user is None:
            user = User(
                company_id=company.id,
                full_name="Administrador del Sistema",
                email="admin@constructora.com",
                password_hash=hash_password("admin123"),
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        exists_user_role = (
            db.query(UserRole)
            .filter(
                UserRole.user_id == user.id,
                UserRole.role_id == role.id,
            )
            .first()
        )

        if exists_user_role is None:
            db.add(
                UserRole(
                    user_id=user.id,
                    role_id=role.id,
                )
            )
            db.commit()

        print("Seed inicial ejecutado correctamente")
        print("Usuario: admin@constructora.com")
        print("Password: admin123")

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()