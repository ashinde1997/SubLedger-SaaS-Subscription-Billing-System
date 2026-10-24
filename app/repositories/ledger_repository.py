from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.ledger_entry import LedgerEntry


class LedgerRepository:
    """Append-only repository for Ledger entries.
    
    In accordance with accounting principles and system design rules,
    Ledger entries are strictly append-only. No update or delete operations are provided.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, entry: LedgerEntry) -> LedgerEntry:
        """Append a new ledger entry."""
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_by_id(self, id: int) -> Optional[LedgerEntry]:
        return self.db.query(LedgerEntry).filter(LedgerEntry.id == id).first()

    def get_by_customer_id(self, customer_id: int) -> List[LedgerEntry]:
        """Fetch all ledger entries for a customer in chronological order."""
        return (
            self.db.query(LedgerEntry)
            .filter(LedgerEntry.customer_id == customer_id)
            .order_by(LedgerEntry.created_at.asc())
            .all()
        )

    def get_by_reference_id(self, reference_id: str) -> List[LedgerEntry]:
        """Fetch ledger entries traceable by reference_id."""
        return (
            self.db.query(LedgerEntry)
            .filter(LedgerEntry.reference_id == reference_id)
            .order_by(LedgerEntry.created_at.asc())
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LedgerEntry]:
        return (
            self.db.query(LedgerEntry)
            .order_by(LedgerEntry.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
