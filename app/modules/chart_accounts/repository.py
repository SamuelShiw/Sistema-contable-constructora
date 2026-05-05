from sqlalchemy.orm import Session

from app.modules.chart_accounts.models import ChartAccount


class ChartAccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, account: ChartAccount) -> ChartAccount:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_all(self) -> list[ChartAccount]:
        return (
            self.db.query(ChartAccount)
            .filter(ChartAccount.is_active.is_(True))
            .order_by(ChartAccount.code)
            .all()
        )

    def get_by_code(self, company_id: int, code: str) -> ChartAccount | None:
        return (
            self.db.query(ChartAccount)
            .filter(
                ChartAccount.company_id == company_id,
                ChartAccount.code == code,
            )
            .first()
        )

    def get_by_id(self, account_id: int) -> ChartAccount | None:
        return self.db.query(ChartAccount).filter(ChartAccount.id == account_id).first()