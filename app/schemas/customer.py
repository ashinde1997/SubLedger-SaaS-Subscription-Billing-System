from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Unique customer email address")
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    company_name: Optional[str] = Field(None, max_length=255)
    status: Optional[Literal["active", "inactive"]] = None


class CustomerResponse(CustomerBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
