from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field


class SubscriptionCreate(BaseModel):
    customer_id: int = Field(..., gt=0, description="Customer ID")
    plan_id: int = Field(..., gt=0, description="Plan ID")
    start_date: Optional[datetime] = Field(None, description="Subscription start date, defaults to current UTC time")


class SubscriptionResponse(BaseModel):
    id: int
    customer_id: int
    plan_id: int
    status: str
    start_date: datetime
    current_period_start: datetime
    current_period_end: datetime
    cancelled_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
