from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.audit.schemas import AuditLogResponse
from app.modules.audit.service import AuditLogService
from app.core.permissions import require_roles
from app.modules.users.models import User

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get("/", response_model=list[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["AUDITOR"])),
) -> list[AuditLogResponse]:
    return AuditLogService(db).list_logs()