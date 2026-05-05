from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    company_id: int
    client_id: int
    name: str
    code: str
    location: str | None = None
    budget: Decimal = Field(default=0, ge=0)
    start_date: date | None = None
    end_date: date | None = None
    status: str = "PLANNED"


class ProjectResponse(BaseModel):
    id: int
    company_id: int
    client_id: int
    name: str
    code: str
    location: str | None
    budget: Decimal
    start_date: date | None
    end_date: date | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }