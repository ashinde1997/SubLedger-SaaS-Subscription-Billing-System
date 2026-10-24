from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True, index=True)
    entry_type = Column(String(50), nullable=False)  # invoice_created, payment_success, payment_failure
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    reference_id = Column(String(255), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    # Relationships
    customer = relationship("Customer", back_populates="ledger_entries")
    invoice = relationship("Invoice", back_populates="ledger_entries")
