from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.accounts_payable.schemas import AccountPayableResponse
from app.modules.audit.service import AuditLogService
from app.modules.purchases.schemas import PurchaseCreate, PurchaseResponse
from app.modules.purchases.service import PurchaseService


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
)


@router.post("/", response_model=PurchaseResponse)
def create_purchase(
    payload: PurchaseCreate,
    db: Session = Depends(get_db),
) -> PurchaseResponse:
    return PurchaseService(db).create_purchase(payload)


@router.get("/", response_model=list[PurchaseResponse])
def list_purchases(
    db: Session = Depends(get_db),
) -> list[PurchaseResponse]:
    return PurchaseService(db).list_purchases()


@router.post("/{purchase_id}/approve", response_model=AccountPayableResponse)
def approve_purchase(
    purchase_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> AccountPayableResponse:
    account_payable = PurchaseService(db).approve_purchase(purchase_id)

    AuditLogService(db).register(
        action="PURCHASE_APPROVE",
        module="PURCHASES",
        table_name="purchases",
        record_id=purchase_id,
        new_data=f"account_payable_id={account_payable.id}",
        ip_address=request.client.host if request.client else None,
    )

    return account_payable