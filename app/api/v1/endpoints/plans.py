from typing import List
from fastapi import APIRouter, Depends, status
from app.api.deps import get_plan_service
from app.services.plan_service import PlanService
from app.schemas.plan import PlanCreate, PlanUpdate, PlanResponse

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    plan_in: PlanCreate,
    plan_service: PlanService = Depends(get_plan_service),
):
    """Create a new subscription plan."""
    return plan_service.create_plan(plan_in)


@router.get("", response_model=List[PlanResponse])
def list_plans(
    skip: int = 0,
    limit: int = 100,
    plan_service: PlanService = Depends(get_plan_service),
):
    """List subscription plans."""
    return plan_service.list_plans(skip=skip, limit=limit)


@router.patch("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    plan_in: PlanUpdate,
    plan_service: PlanService = Depends(get_plan_service),
):
    """Update or deactivate a subscription plan."""
    return plan_service.update_plan(plan_id, plan_in)
