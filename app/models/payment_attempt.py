from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class PaymentAttempt(Base):
    __tablename__ = "payment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(20), nullable=False)  # success, failed
    provider_reference = Column(String(255), nullable=False)
    failure_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    # Relationships
    invoice = relationship("Invoice", back_populates="payment_attempts")
