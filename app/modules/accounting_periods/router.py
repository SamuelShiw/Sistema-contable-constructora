from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.accounting_periods.schemas import (
    AccountingPeriodCreate,
    AccountingPeriodResponse,
)
from app.modules.accounting_periods.service import AccountingPeriodService


router = APIRouter(
    prefix="/accounting-periods",
    tags=["Accounting Periods"],
)


@router.post("/", response_model=AccountingPeriodResponse)
def create_period(
    payload: AccountingPeriodCreate,
    db: Session = Depends(get_db),
) -> AccountingPeriodResponse:
    return AccountingPeriodService(db).create_period(payload)


@router.get("/", response_model=list[AccountingPeriodResponse])
def list_periods(
    db: Session = Depends(get_db),
) -> list[AccountingPeriodResponse]:
    return AccountingPeriodService(db).list_periods()