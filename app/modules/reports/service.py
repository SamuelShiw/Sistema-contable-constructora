from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.accounts_payable.models import AccountPayable
from app.modules.cost_centers.models import CostCenter
from app.modules.projects.models import Project
from app.modules.purchases.models import Purchase
from app.modules.treasury.models import Payment


class ReportsService:
    def __init__(self, db: Session):
        self.db = db

    def project_summary(self) -> list[dict]:
        rows = (
            self.db.query(
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                func.coalesce(func.sum(Purchase.total), 0).label("total_purchases"),
            )
            .outerjoin(Purchase, Purchase.project_id == Project.id)
            .group_by(Project.id, Project.name)
            .all()
        )

        result = []

        for row in rows:
            paid = (
                self.db.query(func.coalesce(func.sum(Payment.amount), 0))
                .join(AccountPayable, Payment.account_payable_id == AccountPayable.id)
                .join(Purchase, AccountPayable.purchase_id == Purchase.id)
                .filter(Purchase.project_id == row.project_id)
                .scalar()
            )

            pending = (
                self.db.query(func.coalesce(func.sum(AccountPayable.balance), 0))
                .join(Purchase, AccountPayable.purchase_id == Purchase.id)
                .filter(Purchase.project_id == row.project_id)
                .scalar()
            )

            result.append(
                {
                    "project_id": row.project_id,
                    "project_name": row.project_name,
                    "total_purchases": row.total_purchases or Decimal("0"),
                    "total_paid": paid or Decimal("0"),
                    "pending_balance": pending or Decimal("0"),
                }
            )

        return result

    def cost_center_summary(self) -> list[dict]:
        rows = (
            self.db.query(
                CostCenter.id.label("cost_center_id"),
                CostCenter.name.label("cost_center_name"),
                func.coalesce(func.sum(Purchase.total), 0).label("total_purchases"),
            )
            .outerjoin(Purchase, Purchase.cost_center_id == CostCenter.id)
            .group_by(CostCenter.id, CostCenter.name)
            .all()
        )

        return [
            {
                "cost_center_id": row.cost_center_id,
                "cost_center_name": row.cost_center_name,
                "total_purchases": row.total_purchases or Decimal("0"),
            }
            for row in rows
        ]

    def accounts_payable_summary(self) -> dict:
        total_amount = (
            self.db.query(func.coalesce(func.sum(AccountPayable.amount), 0)).scalar()
        )

        total_pending = (
            self.db.query(func.coalesce(func.sum(AccountPayable.balance), 0)).scalar()
        )

        total_paid = (
            self.db.query(func.coalesce(func.sum(Payment.amount), 0)).scalar()
        )

        return {
            "total_amount": total_amount or Decimal("0"),
            "total_paid": total_paid or Decimal("0"),
            "total_pending": total_pending or Decimal("0"),
        }