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

    def close_period(self, period_id: int) -> AccountingPeriod:
        period = self.repo.get_by_id(period_id)

        if period is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Periodo contable no encontrado",
            )

        if period.status == "CLOSED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El periodo ya está cerrado",
            )

        if period.status == "LOCKED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El periodo está bloqueado y no puede modificarse",
            )

        if period.status != "OPEN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden cerrar periodos en estado OPEN",
            )

        period.status = "CLOSED"

        return self.repo.save(period)