from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    company_name = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="active")  # active, inactive
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="customer", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="customer", cascade="all, delete-orphan")
    ledger_entries = relationship("LedgerEntry", back_populates="customer", cascade="all, delete-orphan")
