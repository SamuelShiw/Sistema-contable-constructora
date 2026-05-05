from sqlalchemy.orm import Session

from app.modules.companies.models import Company


class CompanyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, company: Company) -> Company:
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_all(self) -> list[Company]:
        return self.db.query(Company).all()