from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.accounting_periods.models import AccountingPeriod
from app.modules.accounting_periods.repository import AccountingPeriodRepository
from app.modules.accounting_periods.schemas import AccountingPeriodCreate


class AccountingPeriodService:
    def __init__(self, db: Session):
        self.repo = AccountingPeriodRepository(db)

    def create_period(self, data: AccountingPeriodCreate) -> AccountingPeriod:
        if data.start_date > data.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio no puede ser mayor a la fecha final",
            )

        period = AccountingPeriod(**data.model_dump())
        return self.repo.create(period)

    def list_periods(self) -> list[AccountingPeriod]:
        return self.repo.get_all()