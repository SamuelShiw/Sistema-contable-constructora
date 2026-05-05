from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.suppliers.schemas import SupplierCreate, SupplierResponse
from app.modules.suppliers.service import SupplierService


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post("/", response_model=SupplierResponse)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
) -> SupplierResponse:
    return SupplierService(db).create_supplier(payload)


@router.get("/", response_model=list[SupplierResponse])
def list_suppliers(
    db: Session = Depends(get_db),
) -> list[SupplierResponse]:
    return SupplierService(db).list_suppliers()