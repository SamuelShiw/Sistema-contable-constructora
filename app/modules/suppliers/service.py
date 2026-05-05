from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.suppliers.models import Supplier
from app.modules.suppliers.repository import SupplierRepository
from app.modules.suppliers.schemas import SupplierCreate


class SupplierService:
    def __init__(self, db: Session):
        self.repo = SupplierRepository(db)

    def create_supplier(self, data: SupplierCreate) -> Supplier:
        existing = self.repo.get_by_ruc(data.ruc)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un proveedor con ese RUC",
            )

        supplier = Supplier(**data.model_dump())
        return self.repo.create(supplier)

    def list_suppliers(self) -> list[Supplier]:
        return self.repo.get_all()