from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.permissions import require_roles

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.audit.service import AuditLogService
from app.modules.journal_entries.schemas import (
    JournalEntryCreate,
    JournalEntryResponse,
)
from app.modules.journal_entries.service import JournalEntryService
from app.modules.users.models import User


router = APIRouter(
    prefix="/journal-entries",
    tags=["Journal Entries"],
)


@router.post("/", response_model=JournalEntryResponse)
def create_entry(
    payload: JournalEntryCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT"])),
) -> JournalEntryResponse:
    entry = JournalEntryService(db).create_entry(
        data=payload,
        created_by=current_user.id,
    )

    AuditLogService(db).register(
        action="CREATE",
        module="JOURNAL_ENTRIES",
        table_name="journal_entries",
        record_id=entry.id,
        user_id=current_user.id,
        new_data=f"entry_number={entry.entry_number}",
        ip_address=request.client.host if request.client else None,
    )

    return entry


@router.get("/", response_model=list[JournalEntryResponse])
def list_entries(
    db: Session = Depends(get_db),
) -> list[JournalEntryResponse]:
    return JournalEntryService(db).list_entries()


@router.post("/{entry_id}/post", response_model=JournalEntryResponse)
def post_entry(
    entry_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT"])),
) -> JournalEntryResponse:
    entry = JournalEntryService(db).post_entry(entry_id)

    AuditLogService(db).register(
        action="POST",
        module="JOURNAL_ENTRIES",
        table_name="journal_entries",
        record_id=entry.id,
        user_id=current_user.id,
        new_data=f"status={entry.status}",
        ip_address=request.client.host if request.client else None,
    )

    return entry


@router.post("/{entry_id}/reverse", response_model=JournalEntryResponse)
def reverse_entry(
    entry_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ACCOUNTANT"])),
) -> JournalEntryResponse:
    reversal = JournalEntryService(db).reverse_entry(
        entry_id=entry_id,
        created_by=current_user.id,
    )

    AuditLogService(db).register(
        action="REVERSE",
        module="JOURNAL_ENTRIES",
        table_name="journal_entries",
        record_id=reversal.id,
        user_id=current_user.id,
        new_data=f"reversed_entry_id={reversal.reversed_entry_id}",
        ip_address=request.client.host if request.client else None,
    )

    return reversal