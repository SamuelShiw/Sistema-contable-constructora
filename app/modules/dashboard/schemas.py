from decimal import Decimal

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_purchases: Decimal
    total_accounts_payable: Decimal
    total_paid: Decimal
    pending_balance: Decimal
    active_projects: int
    open_periods: int