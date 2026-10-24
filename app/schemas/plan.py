from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field


class PlanBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Plan name")
    description: Optional[str] = Field(None, max_length=1000, description="Plan description")
    billing_cycle: Literal["monthly", "quarterly", "yearly"] = Field(
        ..., description="Billing cycle: monthly, quarterly, yearly"
    )
    price: Decimal = Field(..., gt=Decimal("0.00"), description="Plan price, must be strictly greater than 0")
    currency: str = Field("USD", min_length=3, max_length=10, description="ISO Currency code")


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    billing_cycle: Optional[Literal["monthly", "quarterly", "yearly"]] = None
    price: Optional[Decimal] = Field(None, gt=Decimal("0.00"))
    currency: Optional[str] = Field(None, min_length=3, max_length=10)
    status: Optional[Literal["active", "inactive"]] = None


class PlanResponse(PlanBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
