from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.chart_accounts.models import ChartAccount
from app.modules.chart_accounts.repository import ChartAccountRepository
from app.modules.chart_accounts.schemas import ChartAccountCreate


VALID_ACCOUNT_TYPES = {
    "ASSET",
    "LIABILITY",
    "EQUITY",
    "INCOME",
    "EXPENSE",
    "COST",
}


class ChartAccountService:
    def __init__(self, db: Session):
        self.repo = ChartAccountRepository(db)

    def create_account(self, data: ChartAccountCreate) -> ChartAccount:
        if data.account_type not in VALID_ACCOUNT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de cuenta inválido",
            )

        existing = self.repo.get_by_code(
            company_id=data.company_id,
            code=data.code,
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una cuenta con ese código para esta empresa",
            )

        if data.parent_id is not None:
            parent = self.repo.get_by_id(data.parent_id)

            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="La cuenta padre no existe",
                )

            if parent.company_id != data.company_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La cuenta padre pertenece a otra empresa",
                )

        account = ChartAccount(**data.model_dump())
        return self.repo.create(account)

    def list_accounts(self) -> list[ChartAccount]:
        return self.repo.get_all()