from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_subscription_service
from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(
    sub_in: SubscriptionCreate,
    sub_service: SubscriptionService = Depends(get_subscription_service),
):
    """Create and activate a new subscription for a customer."""
    return sub_service.create_subscription(sub_in)


@router.get("", response_model=List[SubscriptionResponse])
def list_subscriptions(
    skip: int = 0,
    limit: int = 100,
    sub_service: SubscriptionService = Depends(get_subscription_service),
):
    """List subscriptions."""
    return sub_service.list_subscriptions(skip=skip, limit=limit)


@router.patch("/{subscription_id}/cancel", response_model=SubscriptionResponse)
def cancel_subscription(
    subscription_id: int,
    sub_service: SubscriptionService = Depends(get_subscription_service),
):
    """Cancel an active subscription."""
    return sub_service.cancel_subscription(subscription_id)
