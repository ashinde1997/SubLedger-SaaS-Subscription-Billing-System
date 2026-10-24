from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class InvoiceGenerateRequest(BaseModel):
    subscription_id: int = Field(..., gt=0, description="Subscription ID to generate invoice for")
    period_start: Optional[datetime] = Field(None, description="Optional custom billing period start")
    period_end: Optional[datetime] = Field(None, description="Optional custom billing period end")
    due_date: Optional[datetime] = Field(None, description="Optional custom due date")


class InvoiceResponse(BaseModel):
    id: int
    subscription_id: int
    customer_id: int
    amount_due: Decimal
    amount_paid: Decimal
    currency: str
    status: str
    period_start: datetime
    period_end: datetime
    due_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
