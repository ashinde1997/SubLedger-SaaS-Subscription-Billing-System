from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_payment_service
from app.services.payment_service import PaymentService
from app.schemas.payment import (
    PaymentRecordRequest,
    PaymentResultResponse,
    PaymentAttemptResponse,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/record", response_model=PaymentResultResponse, status_code=status.HTTP_201_CREATED)
def record_payment(
    request: PaymentRecordRequest,
    payment_service: PaymentService = Depends(get_payment_service),
):
    """Record a payment attempt (success or failed), update invoice status, and log ledger event."""
    attempt, updated_invoice = payment_service.record_payment(request)
    return PaymentResultResponse(
        payment_attempt=PaymentAttemptResponse.model_validate(attempt),
        invoice=updated_invoice,
    )


@router.get("/invoice/{invoice_id}", response_model=List[PaymentAttemptResponse])
def get_payment_attempts_for_invoice(
    invoice_id: int,
    payment_service: PaymentService = Depends(get_payment_service),
):
    """Fetch all payment attempts recorded for a specific invoice."""
    return payment_service.get_payment_attempts_for_invoice(invoice_id)
