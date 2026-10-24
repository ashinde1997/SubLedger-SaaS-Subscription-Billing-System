from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.repositories.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):
    def __init__(self, db: Session):
        super().__init__(Invoice, db)

    def get_by_subscription_id(self, subscription_id: int) -> List[Invoice]:
        return self.db.query(Invoice).filter(Invoice.subscription_id == subscription_id).all()

    def get_by_customer_id(self, customer_id: int) -> List[Invoice]:
        return self.db.query(Invoice).filter(Invoice.customer_id == customer_id).all()
