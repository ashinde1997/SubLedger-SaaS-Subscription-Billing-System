from decimal import Decimal
from typing import List, Optional
from app.exceptions import EntityNotFoundError, BusinessRuleViolationError
from app.models.plan import Plan
from app.repositories.plan_repository import PlanRepository
from app.schemas.plan import PlanCreate, PlanUpdate


class PlanService:
    """Service responsible for subscription plan lifecycle and business rules."""

    def __init__(self, plan_repo: PlanRepository):
        self.plan_repo = plan_repo

    def create_plan(self, plan_in: PlanCreate) -> Plan:
        if plan_in.price <= Decimal("0.00"):
            raise BusinessRuleViolationError("Plan price must be greater than 0.")

        plan = Plan(
            name=plan_in.name,
            description=plan_in.description,
            billing_cycle=plan_in.billing_cycle,
            price=plan_in.price,
            currency=plan_in.currency.upper(),
            status="active",
        )
        return self.plan_repo.create(plan)

    def get_plan(self, plan_id: int) -> Plan:
        plan = self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise EntityNotFoundError(f"Plan with id {plan_id} not found.")
        return plan

    def list_plans(self, skip: int = 0, limit: int = 100) -> List[Plan]:
        return self.plan_repo.get_all(skip=skip, limit=limit)

    def update_plan(self, plan_id: int, plan_in: PlanUpdate) -> Plan:
        plan = self.get_plan(plan_id)

        update_data = plan_in.model_dump(exclude_unset=True)
        if "price" in update_data and update_data["price"] is not None:
            if update_data["price"] <= Decimal("0.00"):
                raise BusinessRuleViolationError("Plan price must be greater than 0.")
            plan.price = update_data["price"]

        if "name" in update_data and update_data["name"] is not None:
            plan.name = update_data["name"]
        if "description" in update_data:
            plan.description = update_data["description"]
        if "billing_cycle" in update_data and update_data["billing_cycle"] is not None:
            plan.billing_cycle = update_data["billing_cycle"]
        if "currency" in update_data and update_data["currency"] is not None:
            plan.currency = update_data["currency"].upper()
        if "status" in update_data and update_data["status"] is not None:
            plan.status = update_data["status"]

        return self.plan_repo.update(plan)

    def deactivate_plan(self, plan_id: int) -> Plan:
        plan = self.get_plan(plan_id)
        plan.status = "inactive"
        return self.plan_repo.update(plan)
