from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.audit.service import AuditLogService
from app.modules.treasury.schemas import PaymentCreate, PaymentResponse
from app.modules.treasury.service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/", response_model=PaymentResponse)
def create_payment(
    payload: PaymentCreate,
    request: Request,
    db: Session = Depends(get_db),
) -> PaymentResponse:
    payment = PaymentService(db).create_payment(payload)

    AuditLogService(db).register(
        action="PAYMENT",
        module="TREASURY",
        table_name="payments",
        record_id=payment.id,
        new_data=f"amount={payment.amount}",
        ip_address=request.client.host if request.client else None,
    )

    return payment


@router.get("/", response_model=list[PaymentResponse])
def list_payments(
    db: Session = Depends(get_db),
) -> list[PaymentResponse]:
    return PaymentService(db).list_payments()