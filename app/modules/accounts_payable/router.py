from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.accounts_payable.repository import AccountPayableRepository
from app.modules.accounts_payable.schemas import AccountPayableResponse
from app.modules.accounts_payable.service import AccountPayableService


router = APIRouter(
    prefix="/accounts-payable",
    tags=["Accounts Payable"],
)


@router.get("/", response_model=list[AccountPayableResponse])
def list_accounts_payable(
    db: Session = Depends(get_db),
) -> list[AccountPayableResponse]:
    repo = AccountPayableRepository(db)
    return AccountPayableService(repo).list_accounts_payable()