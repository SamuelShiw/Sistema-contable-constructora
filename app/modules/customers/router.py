from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.customers.schemas import CustomerCreate, CustomerResponse
from app.modules.customers.service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/", response_model=CustomerResponse)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    return CustomerService(db).create_customer(payload)


@router.get("/", response_model=list[CustomerResponse])
def list_customers(
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    return CustomerService(db).list_customers()