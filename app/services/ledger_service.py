from decimal import Decimal
from typing import List, Optional
from app.exceptions import EntityNotFoundError
from app.models.ledger_entry import LedgerEntry
from app.repositories.ledger_repository import LedgerRepository
from app.repositories.customer_repository import CustomerRepository


class LedgerService:
    """Service managing append-only financial ledger events.
    
    Ensures an immutable audit trail of all billing events (invoicing, payments).
    """

    def __init__(self, ledger_repo: LedgerRepository, customer_repo: CustomerRepository):
        self.ledger_repo = ledger_repo
        self.customer_repo = customer_repo

    def record_entry(
        self,
        customer_id: int,
        entry_type: str,
        amount: Decimal,
        currency: str,
        reference_id: str,
        description: str,
        invoice_id: Optional[int] = None,
    ) -> LedgerEntry:
        """Append an immutable ledger event."""
        entry = LedgerEntry(
            customer_id=customer_id,
            invoice_id=invoice_id,
            entry_type=entry_type,
            amount=amount,
            currency=currency.upper(),
            reference_id=reference_id,
            description=description,
        )
        return self.ledger_repo.create(entry)

    def get_customer_ledger(self, customer_id: int) -> List[LedgerEntry]:
        """Fetch chronological ledger history for a specific customer."""
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundError(f"Customer with id {customer_id} not found.")
        return self.ledger_repo.get_by_customer_id(customer_id)

    def get_entries_by_reference(self, reference_id: str) -> List[LedgerEntry]:
        """Trace ledger records by their external or internal reference id."""
        return self.ledger_repo.get_by_reference_id(reference_id)
