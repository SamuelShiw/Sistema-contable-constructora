from sqlalchemy.orm import Session

from app.modules.audit.models import AuditLog
from app.modules.audit.repository import AuditLogRepository


class AuditLogService:
    def __init__(self, db: Session):
        self.repo = AuditLogRepository(db)

    def register(
        self,
        action: str,
        module: str,
        table_name: str | None = None,
        record_id: int | None = None,
        user_id: int | None = None,
        old_data: str | None = None,
        new_data: str | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            module=module,
            table_name=table_name,
            record_id=record_id,
            old_data=old_data,
            new_data=new_data,
            ip_address=ip_address,
        )

        return self.repo.create(audit_log)

    def list_logs(self) -> list[AuditLog]:
        return self.repo.get_all()