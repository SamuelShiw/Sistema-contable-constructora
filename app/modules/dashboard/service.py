from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.accounts_payable.models import AccountPayable
from app.modules.accounting_periods.models import AccountingPeriod
from app.modules.projects.models import Project
from app.modules.purchases.models import Purchase
from app.modules.treasury.models import Payment


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self) -> dict:
        total_purchases = (
            self.db.query(func.coalesce(func.sum(Purchase.total), 0)).scalar()
        )

        total_accounts_payable = (
            self.db.query(func.coalesce(func.sum(AccountPayable.amount), 0)).scalar()
        )

        total_paid = (
            self.db.query(func.coalesce(func.sum(Payment.amount), 0)).scalar()
        )

        pending_balance = (
            self.db.query(func.coalesce(func.sum(AccountPayable.balance), 0)).scalar()
        )

        active_projects = (
            self.db.query(func.count(Project.id))
            .filter(Project.status.in_(["PLANNED", "IN_PROGRESS", "PAUSED"]))
            .scalar()
        )

        open_periods = (
            self.db.query(func.count(AccountingPeriod.id))
            .filter(AccountingPeriod.status == "OPEN")
            .scalar()
        )

        return {
            "total_purchases": total_purchases or Decimal("0"),
            "total_accounts_payable": total_accounts_payable or Decimal("0"),
            "total_paid": total_paid or Decimal("0"),
            "pending_balance": pending_balance or Decimal("0"),
            "active_projects": active_projects or 0,
            "open_periods": open_periods or 0,
        }