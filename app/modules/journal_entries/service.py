from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.journal_entries.models import JournalEntry, JournalEntryLine
from app.modules.journal_entries.repository import JournalEntryRepository
from app.modules.journal_entries.schemas import JournalEntryCreate


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

    def post_entry(self, entry_id: int) -> JournalEntry:
        entry = self.repo.get_by_id(entry_id)

        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asiento contable no encontrado",
            )

        if entry.status != "DRAFT":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden postear asientos en estado DRAFT",
            )

        entry.status = "POSTED"

        return self.repo.save(entry)

    def reverse_entry(
        self,
        entry_id: int,
        created_by: int,
    ) -> JournalEntry:
        original_entry = self.repo.get_by_id(entry_id)

        if original_entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asiento contable no encontrado",
            )

        if original_entry.status != "POSTED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden revertir asientos en estado POSTED",
            )

        reversal_entry = JournalEntry(
            company_id=original_entry.company_id,
            period_id=original_entry.period_id,
            entry_number=f"{original_entry.entry_number}-REV",
            entry_date=original_entry.entry_date,
            description=f"Reversión de asiento {original_entry.entry_number}",
            status="POSTED",
            source_module="JOURNAL_REVERSAL",
            source_id=original_entry.id,
            created_by=created_by,
            reversed_entry_id=original_entry.id,
        )

        reversal_lines = [
            JournalEntryLine(
                account_id=line.account_id,
                cost_center_id=line.cost_center_id,
                project_id=line.project_id,
                debit=line.credit,
                credit=line.debit,
                description=f"Reversión: {line.description or ''}",
            )
            for line in original_entry.lines
        ]

        original_entry.status = "REVERSED"

        self.repo.save(original_entry)

        return self.repo.create(reversal_entry, reversal_lines)