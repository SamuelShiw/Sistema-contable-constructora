from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.dashboard.schemas import DashboardSummaryResponse
from app.modules.dashboard.service import DashboardService

from app.core.permissions import require_roles
from app.modules.users.models import User


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT", "AUDITOR", "TREASURY"])),
) -> DashboardSummaryResponse:
    return DashboardService(db).get_summary()