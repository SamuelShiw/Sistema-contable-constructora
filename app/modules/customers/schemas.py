from datetime import datetime

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    company_id: int
    document_type: str
    document_number: str
    business_name: str
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None


class CustomerResponse(BaseModel):
    id: int
    company_id: int
    document_type: str
    document_number: str
    business_name: str
    address: str | None
    phone: str | None
    email: EmailStr | None
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }