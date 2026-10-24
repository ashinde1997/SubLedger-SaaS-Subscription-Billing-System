from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.payment_attempt import PaymentAttempt
from app.repositories.base import BaseRepository


class PaymentAttemptRepository(BaseRepository[PaymentAttempt]):
    def __init__(self, db: Session):
        super().__init__(PaymentAttempt, db)

    def get_by_invoice_id(self, invoice_id: int) -> List[PaymentAttempt]:
        return self.db.query(PaymentAttempt).filter(PaymentAttempt.invoice_id == invoice_id).all()

    def get_by_provider_reference(self, provider_reference: str) -> Optional[PaymentAttempt]:
        return (
            self.db.query(PaymentAttempt)
            .filter(PaymentAttempt.provider_reference == provider_reference)
            .first()
        )
