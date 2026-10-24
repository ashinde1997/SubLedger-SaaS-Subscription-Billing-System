from datetime import datetime, timedelta, timezone
from typing import List
from app.exceptions import EntityNotFoundError, BusinessRuleViolationError
from app.models.subscription import Subscription
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.plan_repository import PlanRepository
from app.schemas.subscription import SubscriptionCreate


class SubscriptionService:
    def __init__(
        self,
        subscription_repo: SubscriptionRepository,
        customer_repo: CustomerRepository,
        plan_repo: PlanRepository,
    ):
        self.subscription_repo = subscription_repo
        self.customer_repo = customer_repo
        self.plan_repo = plan_repo

    def create_subscription(self, sub_in: SubscriptionCreate) -> Subscription:
        customer = self.customer_repo.get_by_id(sub_in.customer_id)
        if not customer:
            raise EntityNotFoundError(f"Customer #{sub_in.customer_id} not found.")
        if customer.status != "active":
            raise BusinessRuleViolationError("Cannot activate subscription for an inactive customer account.")

        plan = self.plan_repo.get_by_id(sub_in.plan_id)
        if not plan:
            raise EntityNotFoundError(f"Plan #{sub_in.plan_id} not found.")

        if plan.status != "active":
            raise BusinessRuleViolationError("A subscription cannot be created for an inactive plan.")

        # Avoid redundant active subscriptions to the same tier
        existing_active = self.subscription_repo.get_active_by_customer_and_plan(
            customer_id=sub_in.customer_id, plan_id=sub_in.plan_id
        )
        if existing_active:
            raise BusinessRuleViolationError(
                f"Customer #{sub_in.customer_id} already has an active subscription to plan #{sub_in.plan_id}."
            )

        start_date = sub_in.start_date or datetime.now(timezone.utc)
        current_period_start = start_date

        cycle_durations = {
            "monthly": 30,
            "quarterly": 90,
            "yearly": 365,
        }
        days_to_add = cycle_durations.get(plan.billing_cycle, 30)
        current_period_end = current_period_start + timedelta(days=days_to_add)

        subscription = Subscription(
            customer_id=sub_in.customer_id,
            plan_id=sub_in.plan_id,
            status="active",
            start_date=start_date,
            current_period_start=current_period_start,
            current_period_end=current_period_end,
            cancelled_at=None,
        )
        return self.subscription_repo.create(subscription)

    def cancel_subscription(self, subscription_id: int) -> Subscription:
        subscription = self.subscription_repo.get_by_id(subscription_id)
        if not subscription:
            raise EntityNotFoundError(f"Subscription #{subscription_id} not found.")

        if subscription.status == "cancelled":
            raise BusinessRuleViolationError(f"Subscription #{subscription_id} has already been cancelled.")

        return self.subscription_repo.cancel(subscription)

    def get_subscription(self, subscription_id: int) -> Subscription:
        sub = self.subscription_repo.get_by_id(subscription_id)
        if not sub:
            raise EntityNotFoundError(f"Subscription #{subscription_id} not found.")
        return sub

    def list_subscriptions(self, skip: int = 0, limit: int = 100) -> List[Subscription]:
        return self.subscription_repo.get_all(skip=skip, limit=limit)
