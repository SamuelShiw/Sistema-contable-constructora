from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.audit.schemas import AuditLogResponse
from app.modules.audit.service import AuditLogService


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get("/", response_model=list[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
) -> list[AuditLogResponse]:
    return AuditLogService(db).list_logs()