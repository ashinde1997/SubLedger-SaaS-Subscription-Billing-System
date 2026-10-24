from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.repositories.base import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self, db: Session):
        super().__init__(Subscription, db)

    def get_active_by_customer_and_plan(self, customer_id: int, plan_id: int) -> Optional[Subscription]:
        """Find an active subscription for the given customer and plan."""
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.plan_id == plan_id,
                Subscription.status == "active",
            )
            .first()
        )

    def get_by_customer(self, customer_id: int) -> List[Subscription]:
        return self.db.query(Subscription).filter(Subscription.customer_id == customer_id).all()

    def cancel(self, subscription: Subscription) -> Subscription:
        subscription.status = "cancelled"
        subscription.cancelled_at = datetime.now(timezone.utc)
        return self.update(subscription)
