from datetime import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    business_name: str
    ruc: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    legal_representative: str | None = None
    currency: str = "PEN"


class CompanyResponse(BaseModel):
    id: int
    business_name: str
    ruc: str
    currency: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }