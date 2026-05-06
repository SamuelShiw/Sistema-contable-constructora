from decimal import Decimal

from pydantic import BaseModel


class ProjectSummaryResponse(BaseModel):
    project_id: int
    project_name: str
    total_purchases: Decimal
    total_paid: Decimal
    pending_balance: Decimal


class CostCenterSummaryResponse(BaseModel):
    cost_center_id: int
    cost_center_name: str
    total_purchases: Decimal


class AccountsPayableSummaryResponse(BaseModel):
    total_amount: Decimal
    total_paid: Decimal
    total_pending: Decimal