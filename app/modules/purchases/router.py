from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.accounts_payable.schemas import AccountPayableResponse
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
    db: Session = Depends(get_db),
) -> AccountPayableResponse:
    return PurchaseService(db).approve_purchase(purchase_id)