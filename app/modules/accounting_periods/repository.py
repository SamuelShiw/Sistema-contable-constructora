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