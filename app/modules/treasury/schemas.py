from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    account_payable_id: int
    payment_date: date
    payment_method: str
    amount: Decimal = Field(gt=0)
    reference: str | None = None


class PaymentResponse(BaseModel):
    id: int
    company_id: int
    supplier_id: int
    account_payable_id: int
    payment_date: date
    payment_method: str
    amount: Decimal
    reference: str | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }