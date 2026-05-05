from datetime import datetime

from pydantic import BaseModel, EmailStr


class SupplierCreate(BaseModel):
    company_id: int
    ruc: str
    business_name: str
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None


class SupplierResponse(BaseModel):
    id: int
    company_id: int
    ruc: str
    business_name: str
    address: str | None
    phone: str | None
    email: EmailStr | None
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }