from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from app.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    billing_cycle = Column(String(50), nullable=False)  # monthly, quarterly, yearly
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(20), nullable=False, default="active")  # active, inactive
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan", cascade="all, delete-orphan")
