from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.journal_entries.models import JournalEntry, JournalEntryLine
from app.modules.journal_entries.repository import JournalEntryRepository
from app.modules.journal_entries.schemas import JournalEntryCreate


VALID_JOURNAL_STATUSES = {
    "DRAFT",
    "POSTED",
    "REVERSED",
    "CANCELLED",
}


class JournalEntryService:
    def __init__(self, db: Session):
        self.repo = JournalEntryRepository(db)

    def create_entry(
        self,
        data: JournalEntryCreate,
        created_by: int,
    ) -> JournalEntry:
        if len(data.lines) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un asiento debe tener al menos dos líneas",
            )

        total_debit = sum((line.debit for line in data.lines), Decimal("0"))
        total_credit = sum((line.credit for line in data.lines), Decimal("0"))

        if total_debit != total_credit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El total debe ser igual al total haber",
            )

        entry = JournalEntry(
            company_id=data.company_id,
            period_id=data.period_id,
            entry_number=data.entry_number,
            entry_date=data.entry_date,
            description=data.description,
            source_module=data.source_module,
            source_id=data.source_id,
            created_by=created_by,
            status="DRAFT",
        )

        lines = [
            JournalEntryLine(
                account_id=line.account_id,
                cost_center_id=line.cost_center_id,
                project_id=line.project_id,
                debit=line.debit,
                credit=line.credit,
                description=line.description,
            )
            for line in data.lines
        ]

        return self.repo.create(entry, lines)

    def list_entries(self) -> list[JournalEntry]:
        return self.repo.get_all()