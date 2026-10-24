from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="active")  # active, cancelled
    start_date = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    current_period_start = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")
