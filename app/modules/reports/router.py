from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.reports.schemas import (
    AccountsPayableSummaryResponse,
    CostCenterSummaryResponse,
    ProjectSummaryResponse,
)
from app.modules.reports.service import ReportsService
from app.core.permissions import require_roles
from app.modules.users.models import User


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/projects-summary", response_model=list[ProjectSummaryResponse])
def project_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT", "AUDITOR"])),
) -> list[ProjectSummaryResponse]:
    return ReportsService(db).project_summary()


@router.get("/cost-centers-summary", response_model=list[CostCenterSummaryResponse])
def cost_center_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT", "AUDITOR"])),
) -> list[CostCenterSummaryResponse]:
    return ReportsService(db).cost_center_summary()


@router.get("/accounts-payable-summary", response_model=AccountsPayableSummaryResponse)
def accounts_payable_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT", "AUDITOR"])),
) -> AccountsPayableSummaryResponse:
    return ReportsService(db).accounts_payable_summary()