from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_customer_service, get_ledger_service
from app.services.customer_service import CustomerService
from app.services.ledger_service import LedgerService
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.ledger import LedgerEntryResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    customer_service: CustomerService = Depends(get_customer_service),
):
    """Create a new customer."""
    return customer_service.create_customer(customer_in)


@router.get("", response_model=List[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    customer_service: CustomerService = Depends(get_customer_service),
):
    """List all customers."""
    return customer_service.list_customers(skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    customer_service: CustomerService = Depends(get_customer_service),
):
    """Fetch customer details by ID."""
    return customer_service.get_customer(customer_id)


@router.get("/{customer_id}/ledger", response_model=List[LedgerEntryResponse])
def get_customer_ledger(
    customer_id: int,
    ledger_service: LedgerService = Depends(get_ledger_service),
):
    """Fetch complete append-only ledger history for a specific customer."""
    return ledger_service.get_customer_ledger(customer_id)
