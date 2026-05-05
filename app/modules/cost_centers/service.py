from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.cost_centers.models import CostCenter
from app.modules.cost_centers.repository import CostCenterRepository
from app.modules.cost_centers.schemas import CostCenterCreate


class CostCenterService:
    def __init__(self, db: Session):
        self.repo = CostCenterRepository(db)

    def create_cost_center(self, data: CostCenterCreate) -> CostCenter:
        existing = self.repo.get_by_code(data.code)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un centro de costo con ese código",
            )

        cost_center = CostCenter(**data.model_dump())
        return self.repo.create(cost_center)

    def list_cost_centers(self) -> list[CostCenter]:
        return self.repo.get_all()