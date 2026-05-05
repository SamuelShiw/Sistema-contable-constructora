from sqlalchemy.orm import Session

from app.modules.companies.models import Company
from app.modules.companies.repository import CompanyRepository
from app.modules.companies.schemas import CompanyCreate


class CompanyService:
    def __init__(self, db: Session):
        self.repo = CompanyRepository(db)

    def create_company(self, data: CompanyCreate) -> Company:
        company = Company(**data.model_dump())
        return self.repo.create(company)

    def list_companies(self) -> list[Company]:
        return self.repo.get_all()