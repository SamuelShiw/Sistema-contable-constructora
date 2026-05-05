from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.companies.schemas import CompanyCreate, CompanyResponse
from app.modules.companies.service import CompanyService


router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.post("/", response_model=CompanyResponse)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
) -> CompanyResponse:
    return CompanyService(db).create_company(payload)


@router.get("/", response_model=list[CompanyResponse])
def list_companies(
    db: Session = Depends(get_db),
) -> list[CompanyResponse]:
    return CompanyService(db).list_companies()