from sqlalchemy.orm import Session

from app.modules.purchases.models import Purchase, PurchaseDetail


class PurchaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        purchase: Purchase,
        details: list[PurchaseDetail],
    ) -> Purchase:
        self.db.add(purchase)
        self.db.flush()

        for detail in details:
            detail.purchase_id = purchase.id
            self.db.add(detail)

        self.db.commit()
        self.db.refresh(purchase)
        return purchase

    def get_all(self) -> list[Purchase]:
        return (
            self.db.query(Purchase)
            .order_by(Purchase.issue_date.desc())
            .all()
        )

    def get_by_id(self, purchase_id: int) -> Purchase | None:
        return (
            self.db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

    def get_by_document(
        self,
        supplier_id: int,
        document_number: str,
    ) -> Purchase | None:
        return (
            self.db.query(Purchase)
            .filter(
                Purchase.supplier_id == supplier_id,
                Purchase.document_number == document_number,
            )
            .first()
        )

    def save(self, purchase: Purchase) -> Purchase:
        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)
        return purchase