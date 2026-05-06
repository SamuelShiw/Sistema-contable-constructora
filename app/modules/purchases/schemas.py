from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class PurchaseDetailCreate(BaseModel):
    description: str
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(ge=0)


class PurchaseCreate(BaseModel):
    company_id: int
    supplier_id: int
    project_id: int
    cost_center_id: int
    document_type: str
    document_number: str
    issue_date: date
    due_date: date | None = None
    details: list[PurchaseDetailCreate]

    @model_validator(mode="after")
    def validate_details(self) -> "PurchaseCreate":
        if len(self.details) == 0:
            raise ValueError("La compra debe tener al menos un detalle")
        return self


class PurchaseDetailResponse(BaseModel):
    id: int
    description: str
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True,
    }


class PurchaseResponse(BaseModel):
    id: int
    company_id: int
    supplier_id: int
    project_id: int
    cost_center_id: int
    document_type: str
    document_number: str
    issue_date: date
    due_date: date | None
    subtotal: Decimal
    igv: Decimal
    total: Decimal
    status: str
    created_at: datetime
    details: list[PurchaseDetailResponse]

    model_config = {
        "from_attributes": True,
    }