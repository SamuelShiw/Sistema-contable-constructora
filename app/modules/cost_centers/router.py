from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.cost_centers.schemas import CostCenterCreate, CostCenterResponse
from app.modules.cost_centers.service import CostCenterService


router = APIRouter(
    prefix="/cost-centers",
    tags=["Cost Centers"],
)


@router.post("/", response_model=CostCenterResponse)
def create_cost_center(
    payload: CostCenterCreate,
    db: Session = Depends(get_db),
) -> CostCenterResponse:
    return CostCenterService(db).create_cost_center(payload)


@router.get("/", response_model=list[CostCenterResponse])
def list_cost_centers(
    db: Session = Depends(get_db),
) -> list[CostCenterResponse]:
    return CostCenterService(db).list_cost_centers()