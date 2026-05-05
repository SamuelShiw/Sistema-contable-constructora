from sqlalchemy.orm import Session, selectinload

from app.modules.journal_entries.models import JournalEntry, JournalEntryLine


class JournalEntryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        entry: JournalEntry,
        lines: list[JournalEntryLine],
    ) -> JournalEntry:
        self.db.add(entry)
        self.db.flush()

        for line in lines:
            line.journal_entry_id = entry.id
            self.db.add(line)

        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_all(self) -> list[JournalEntry]:
        return (
            self.db.query(JournalEntry)
            .order_by(JournalEntry.entry_date.desc())
            .all()
        )

    def get_by_id(self, entry_id: int) -> JournalEntry | None:
        return (
            self.db.query(JournalEntry)
            .filter(JournalEntry.id == entry_id)
            .first()
        )