from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_invoice_service
from app.services.invoice_service import InvoiceService
from app.schemas.invoice import InvoiceGenerateRequest, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/generate", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def generate_invoice(
    request: InvoiceGenerateRequest,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    """Generate an invoice for an active subscription and record invoice_created ledger event."""
    return invoice_service.generate_invoice(request)


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(
    skip: int = 0,
    limit: int = 100,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    """List invoices."""
    return invoice_service.list_invoices(skip=skip, limit=limit)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    invoice_service: InvoiceService = Depends(get_invoice_service),
):
    """Fetch invoice details by invoice ID."""
    return invoice_service.get_invoice(invoice_id)
