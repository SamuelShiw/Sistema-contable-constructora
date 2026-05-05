from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)

    period_id: Mapped[int] = mapped_column(
        ForeignKey("accounting_periods.id"),
        nullable=False,
    )

    entry_number: Mapped[str] = mapped_column(String(50), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[str] = mapped_column(String(20), default="DRAFT")

    source_module: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    reversed_entry_id: Mapped[int | None] = mapped_column(
        ForeignKey("journal_entries.id"),
        nullable=True,
    )

    lines: Mapped[list["JournalEntryLine"]] = relationship(
        back_populates="entry",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class JournalEntryLine(Base):
    __tablename__ = "journal_entry_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    journal_entry_id: Mapped[int] = mapped_column(
        ForeignKey("journal_entries.id"),
        nullable=False,
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("chart_accounts.id"),
        nullable=False,
    )

    cost_center_id: Mapped[int | None] = mapped_column(
        ForeignKey("cost_centers.id"),
        nullable=True,
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
    )

    debit: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    credit: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    entry: Mapped["JournalEntry"] = relationship(
        back_populates="lines",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)