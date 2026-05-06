from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountPayableResponse(BaseModel):
    id: int
    company_id: int
    supplier_id: int
    purchase_id: int
    amount: Decimal
    balance: Decimal
    due_date: date | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }