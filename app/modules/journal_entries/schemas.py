from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class JournalEntryLineCreate(BaseModel):
    account_id: int
    cost_center_id: int | None = None
    project_id: int | None = None
    debit: Decimal = Field(default=0, ge=0)
    credit: Decimal = Field(default=0, ge=0)
    description: str | None = None

    @model_validator(mode="after")
    def validate_debit_credit(self) -> "JournalEntryLineCreate":
        if self.debit > 0 and self.credit > 0:
            raise ValueError("Una línea no puede tener debe y haber al mismo tiempo")

        if self.debit == 0 and self.credit == 0:
            raise ValueError("Una línea debe tener debe o haber")

        return self


class JournalEntryCreate(BaseModel):
    company_id: int
    period_id: int
    entry_number: str
    entry_date: date
    description: str
    source_module: str | None = None
    source_id: int | None = None
    lines: list[JournalEntryLineCreate]


class JournalEntryLineResponse(BaseModel):
    id: int
    account_id: int
    cost_center_id: int | None
    project_id: int | None
    debit: Decimal
    credit: Decimal
    description: str | None

    model_config = {
        "from_attributes": True,
    }


class JournalEntryResponse(BaseModel):
    id: int
    company_id: int
    period_id: int
    entry_number: str
    entry_date: date
    description: str
    status: str
    source_module: str | None
    source_id: int | None
    created_by: int
    reversed_entry_id: int | None
    created_at: datetime
    lines: list[JournalEntryLineResponse]

    model_config = {
        "from_attributes": True,
    }