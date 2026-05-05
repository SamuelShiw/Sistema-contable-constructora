from datetime import date, datetime

from pydantic import BaseModel, Field


class AccountingPeriodCreate(BaseModel):
    company_id: int
    year: int = Field(ge=2000, le=2100)
    month: int = Field(ge=1, le=12)
    start_date: date
    end_date: date


class AccountingPeriodResponse(BaseModel):
    id: int
    company_id: int
    year: int
    month: int
    start_date: date
    end_date: date
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }