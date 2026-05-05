from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JournalEntryResponse:
    return JournalEntryService(db).create_entry(
        data=payload,
        created_by=current_user.id,
    )


@router.get("/", response_model=list[JournalEntryResponse])
def list_entries(
    db: Session = Depends(get_db),
) -> list[JournalEntryResponse]:
    return JournalEntryService(db).list_entries()