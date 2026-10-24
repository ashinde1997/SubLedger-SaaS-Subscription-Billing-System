from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    amount_due = Column(Numeric(12, 2), nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False, default=0.00)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(30), nullable=False, default="issued")  # draft, issued, partially_paid, paid, overdue, void
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")
    payment_attempts = relationship("PaymentAttempt", back_populates="invoice", cascade="all, delete-orphan")
    ledger_entries = relationship("LedgerEntry", back_populates="invoice")
