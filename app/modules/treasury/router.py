from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.treasury.schemas import PaymentCreate, PaymentResponse
from app.modules.treasury.service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/", response_model=PaymentResponse)
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
) -> PaymentResponse:
    return PaymentService(db).create_payment(payload)


@router.get("/", response_model=list[PaymentResponse])
def list_payments(
    db: Session = Depends(get_db),
) -> list[PaymentResponse]:
    return PaymentService(db).list_payments()