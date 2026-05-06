from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    module: str
    table_name: str | None
    record_id: int | None
    old_data: str | None
    new_data: str | None
    ip_address: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }