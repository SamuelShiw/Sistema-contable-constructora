from sqlalchemy.orm import Session

from app.modules.cost_centers.models import CostCenter


class CostCenterRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cost_center: CostCenter) -> CostCenter:
        self.db.add(cost_center)
        self.db.commit()
        self.db.refresh(cost_center)
        return cost_center

    def get_all(self) -> list[CostCenter]:
        return self.db.query(CostCenter).filter(CostCenter.is_active.is_(True)).all()

    def get_by_code(self, code: str) -> CostCenter | None:
        return self.db.query(CostCenter).filter(CostCenter.code == code).first()