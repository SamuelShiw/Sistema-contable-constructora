from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    id: int
    company_id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }