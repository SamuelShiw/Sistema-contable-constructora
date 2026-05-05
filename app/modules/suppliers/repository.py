from sqlalchemy.orm import Session

from app.modules.suppliers.models import Supplier


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, supplier: Supplier) -> Supplier:
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def get_all(self) -> list[Supplier]:
        return self.db.query(Supplier).filter(Supplier.is_active.is_(True)).all()

    def get_by_ruc(self, ruc: str) -> Supplier | None:
        return self.db.query(Supplier).filter(Supplier.ruc == ruc).first()