from sqlalchemy.orm import Session

from app.modules.accounting_periods.models import AccountingPeriod


class AccountingPeriodRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, period: AccountingPeriod) -> AccountingPeriod:
        self.db.add(period)
        self.db.commit()
        self.db.refresh(period)
        return period

    def get_all(self) -> list[AccountingPeriod]:
        return self.db.query(AccountingPeriod).all()

    def get_by_id(self, period_id: int) -> AccountingPeriod | None:
        return (
            self.db.query(AccountingPeriod)
            .filter(AccountingPeriod.id == period_id)
            .first()
        )

    def ensure_open_period(self, period_id: int) -> AccountingPeriod:
        period = self.get_by_id(period_id)

        if period is None:
            raise ValueError("PERIOD_NOT_FOUND")

        if period.status != "OPEN":
            raise ValueError("PERIOD_NOT_OPEN")

        return period

    def save(self, period: AccountingPeriod) -> AccountingPeriod:
        self.db.add(period)
        self.db.commit()
        self.db.refresh(period)
        return period