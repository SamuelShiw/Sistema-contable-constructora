from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.chart_accounts.schemas import (
    ChartAccountCreate,
    ChartAccountResponse,
)
from app.modules.chart_accounts.service import ChartAccountService


router = APIRouter(
    prefix="/chart-accounts",
    tags=["Chart Accounts"],
)


@router.post("/", response_model=ChartAccountResponse)
def create_account(
    payload: ChartAccountCreate,
    db: Session = Depends(get_db),
) -> ChartAccountResponse:
    return ChartAccountService(db).create_account(payload)


@router.get("/", response_model=list[ChartAccountResponse])
def list_accounts(
    db: Session = Depends(get_db),
) -> list[ChartAccountResponse]:
    return ChartAccountService(db).list_accounts()