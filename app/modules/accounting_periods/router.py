from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.accounting_periods.schemas import (
    AccountingPeriodCreate,
    AccountingPeriodResponse,
)
from app.modules.accounting_periods.service import AccountingPeriodService
from app.modules.audit.service import AuditLogService
from app.modules.users.models import User


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


@router.post("/{period_id}/close", response_model=AccountingPeriodResponse)
def close_period(
    period_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AccountingPeriodResponse:
    period = AccountingPeriodService(db).close_period(period_id)

    AuditLogService(db).register(
        action="CLOSE_PERIOD",
        module="ACCOUNTING_PERIODS",
        table_name="accounting_periods",
        record_id=period.id,
        user_id=current_user.id,
        new_data=f"status={period.status}",
        ip_address=request.client.host if request.client else None,
    )

    return period