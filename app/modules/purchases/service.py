from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.purchases.models import Purchase, PurchaseDetail
from app.modules.purchases.repository import PurchaseRepository
from app.modules.purchases.schemas import PurchaseCreate


IGV_RATE = Decimal("0.18")


class PurchaseService:
    def __init__(self, db: Session):
        self.repo = PurchaseRepository(db)

    def create_purchase(self, data: PurchaseCreate) -> Purchase:
        existing = self.repo.get_by_document(
            supplier_id=data.supplier_id,
            document_number=data.document_number,
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una compra con ese documento para este proveedor",
            )

        details: list[PurchaseDetail] = []

        subtotal = Decimal("0")

        for item in data.details:
            line_subtotal = item.quantity * item.unit_price
            subtotal += line_subtotal

            details.append(
                PurchaseDetail(
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=line_subtotal,
                )
            )

        igv = subtotal * IGV_RATE
        total = subtotal + igv

        purchase = Purchase(
            company_id=data.company_id,
            supplier_id=data.supplier_id,
            project_id=data.project_id,
            cost_center_id=data.cost_center_id,
            document_type=data.document_type,
            document_number=data.document_number,
            issue_date=data.issue_date,
            due_date=data.due_date,
            subtotal=subtotal,
            igv=igv,
            total=total,
            status="DRAFT",
        )

        return self.repo.create(purchase, details)

    def list_purchases(self) -> list[Purchase]:
        return self.repo.get_all()