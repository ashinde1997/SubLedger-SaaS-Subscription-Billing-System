from datetime import datetime, timedelta, timezone
from typing import Optional, List
from app.exceptions import EntityNotFoundError, BusinessRuleViolationError
from app.models.invoice import Invoice
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.plan_repository import PlanRepository
from app.services.ledger_service import LedgerService
from app.schemas.invoice import InvoiceGenerateRequest


class InvoiceService:
    def __init__(
        self,
        subscription_repo: SubscriptionRepository,
        plan_repo: PlanRepository,
        invoice_repo: InvoiceRepository,
        ledger_service: LedgerService,
    ):
        self.subscription_repo = subscription_repo
        self.plan_repo = plan_repo
        self.invoice_repo = invoice_repo
        self.ledger_service = ledger_service

    def generate_invoice(self, request: InvoiceGenerateRequest) -> Invoice:
        subscription = self.subscription_repo.get_by_id(request.subscription_id)
        if not subscription:
            raise EntityNotFoundError(f"Subscription #{request.subscription_id} not found.")

        if subscription.status != "active":
            raise BusinessRuleViolationError(
                f"Cannot generate invoice for subscription #{subscription.id} because status is '{subscription.status}'."
            )

        plan = self.plan_repo.get_by_id(subscription.plan_id)
        if not plan:
            raise EntityNotFoundError(f"Associated plan #{subscription.plan_id} not found.")

        # Capture a static price snapshot from the plan at billing time
        now = datetime.now(timezone.utc)
        amount_due = plan.price
        period_start = request.period_start or subscription.current_period_start
        period_end = request.period_end or subscription.current_period_end
        due_date = request.due_date or (now + timedelta(days=14))

        invoice = Invoice(
            subscription_id=subscription.id,
            customer_id=subscription.customer_id,
            amount_due=amount_due,
            amount_paid=0.00,
            currency=plan.currency,
            status="issued",
            period_start=period_start,
            period_end=period_end,
            due_date=due_date,
            created_at=now,
        )
        created_invoice = self.invoice_repo.create(invoice)

        # Append invoice creation to the immutable customer ledger
        self.ledger_service.record_entry(
            customer_id=subscription.customer_id,
            invoice_id=created_invoice.id,
            entry_type="invoice_created",
            amount=created_invoice.amount_due,
            currency=created_invoice.currency,
            reference_id=f"INV-{created_invoice.id}",
            description=f"Invoice #{created_invoice.id} generated for subscription #{subscription.id}",
        )

        return created_invoice

    def get_invoice(self, invoice_id: int) -> Invoice:
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise EntityNotFoundError(f"Invoice #{invoice_id} not found.")
        return invoice

    def list_invoices(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.invoice_repo.get_all(skip=skip, limit=limit)
