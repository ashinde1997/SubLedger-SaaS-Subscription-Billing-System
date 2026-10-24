from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.invoice import InvoiceResponse


class PaymentRecordRequest(BaseModel):
    invoice_id: int = Field(..., gt=0, description="Invoice ID to apply payment to")
    amount: Decimal = Field(..., gt=Decimal("0.00"), description="Payment amount, strictly greater than 0")
    currency: str = Field("USD", min_length=3, max_length=10, description="Currency code")
    status: Literal["success", "failed"] = Field(..., description="Payment status: success or failed")
    provider_reference: str = Field(..., min_length=1, max_length=255, description="External provider payment reference")
    failure_reason: Optional[str] = Field(None, max_length=500, description="Reason if payment failed")


class PaymentAttemptResponse(BaseModel):
    id: int
    invoice_id: int
    amount: Decimal
    currency: str
    status: str
    provider_reference: str
    failure_reason: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentResultResponse(BaseModel):
    payment_attempt: PaymentAttemptResponse
    invoice: InvoiceResponse
