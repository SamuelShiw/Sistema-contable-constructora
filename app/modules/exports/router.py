from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.exports.service import ExportService


router = APIRouter(
    prefix="/exports",
    tags=["Exports"],
)


@router.get("/purchases/excel")
def export_purchases_excel(
    db: Session = Depends(get_db),
):
    stream = ExportService(db).export_purchases_excel()

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=purchases.xlsx"
        },
    )


@router.get("/accounts-payable/excel")
def export_accounts_payable_excel(
    db: Session = Depends(get_db),
):
    stream = ExportService(db).export_accounts_payable_excel()

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=accounts_payable.xlsx"
        },
    )


@router.get("/dashboard/pdf")
def export_dashboard_pdf(
    db: Session = Depends(get_db),
):
    stream = ExportService(db).export_dashboard_pdf()

    return StreamingResponse(
        stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=dashboard.pdf"
        },
    )