from sqlalchemy.orm import Session

from app.modules.accounts_payable.models import AccountPayable


class AccountPayableRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, account: AccountPayable) -> AccountPayable:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_all(self) -> list[AccountPayable]:
        return (
            self.db.query(AccountPayable)
            .order_by(AccountPayable.created_at.desc())
            .all()
        )

    def get_by_id(self, account_id: int) -> AccountPayable | None:
        return (
            self.db.query(AccountPayable)
            .filter(AccountPayable.id == account_id)
            .first()
        )

    def get_by_purchase_id(self, purchase_id: int) -> AccountPayable | None:
        return (
            self.db.query(AccountPayable)
            .filter(AccountPayable.purchase_id == purchase_id)
            .first()
        )

    def save(self, account: AccountPayable) -> AccountPayable:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account