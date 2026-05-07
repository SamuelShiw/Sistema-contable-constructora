from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.dashboard.schemas import DashboardSummaryResponse
from app.modules.dashboard.service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(
    db: Session = Depends(get_db),
) -> DashboardSummaryResponse:
    return DashboardService(db).get_summary()