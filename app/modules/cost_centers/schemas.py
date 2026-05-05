from datetime import datetime

from pydantic import BaseModel


class CostCenterCreate(BaseModel):
    company_id: int
    project_id: int
    code: str
    name: str
    type: str


class CostCenterResponse(BaseModel):
    id: int
    company_id: int
    project_id: int
    code: str
    name: str
    type: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }