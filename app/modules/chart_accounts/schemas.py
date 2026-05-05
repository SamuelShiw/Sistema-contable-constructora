from datetime import datetime

from pydantic import BaseModel, Field


class ChartAccountCreate(BaseModel):
    company_id: int
    code: str
    name: str
    account_type: str
    parent_id: int | None = None
    level: int = Field(ge=1)
    is_movement: bool = True


class ChartAccountResponse(BaseModel):
    id: int
    company_id: int
    code: str
    name: str
    account_type: str
    parent_id: int | None
    level: int
    is_movement: bool
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }