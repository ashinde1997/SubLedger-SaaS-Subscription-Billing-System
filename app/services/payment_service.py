from decimal import Decimal
from typing import Tuple, List, Optional
from app.exceptions import EntityNotFoundError, BusinessRuleViolationError
from app.models.payment_attempt import PaymentAttempt
from app.models.invoice import Invoice
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.payment_attempt_repository import PaymentAttemptRepository
from app.services.ledger_service import LedgerService
from app.schemas.payment import PaymentRecordRequest


class PaymentService:
    def __init__(
        self,
        invoice_repo: InvoiceRepository,
        payment_attempt_repo: PaymentAttemptRepository,
        ledger_service: LedgerService,
    ):
        self.invoice_repo = invoice_repo
        self.payment_attempt_repo = payment_attempt_repo
        self.ledger_service = ledger_service

    def record_payment(self, request: PaymentRecordRequest) -> Tuple[PaymentAttempt, Invoice]:
        invoice = self.invoice_repo.get_by_id(request.invoice_id)
        if not invoice:
            raise EntityNotFoundError(f"Invoice #{request.invoice_id} not found.")

        if invoice.status == "void":
            raise BusinessRuleViolationError("Cannot record payments on a voided invoice.")

        remaining_unpaid = Decimal(str(invoice.amount_due)) - Decimal(str(invoice.amount_paid))

        # Disallow overpayments or payments on settled accounts
        if request.status == "success":
            if remaining_unpaid <= Decimal("0.00"):
                raise BusinessRuleViolationError(
                    f"Invoice #{invoice.id} is already fully paid."
                )
            if request.amount > remaining_unpaid:
                raise BusinessRuleViolationError(
                    f"Payment amount ({request.amount}) cannot exceed the remaining unpaid amount ({remaining_unpaid}) on invoice #{invoice.id}."
                )

        # Log attempt record
        payment_attempt = PaymentAttempt(
            invoice_id=invoice.id,
            amount=request.amount,
            currency=request.currency.upper(),
            status=request.status,
            provider_reference=request.provider_reference,
            failure_reason=request.failure_reason if request.status == "failed" else None,
        )
        created_attempt = self.payment_attempt_repo.create(payment_attempt)

        # Adjust balances and statuses only if transaction was successful
        if request.status == "success":
            new_amount_paid = Decimal(str(invoice.amount_paid)) + request.amount
            invoice.amount_paid = new_amount_paid
            invoice.status = "paid" if new_amount_paid >= Decimal(str(invoice.amount_due)) else "partially_paid"
            invoice = self.invoice_repo.update(invoice)

        # Audit trail: append success or failure to ledger
        entry_type = "payment_success" if request.status == "success" else "payment_failure"
        description = (
            f"Payment of {request.currency.upper()} {request.amount} confirmed (Ref: {request.provider_reference})"
            if request.status == "success"
            else f"Payment of {request.currency.upper()} {request.amount} failed: {request.failure_reason or 'Declined'}"
        )

        self.ledger_service.record_entry(
            customer_id=invoice.customer_id,
            invoice_id=invoice.id,
            entry_type=entry_type,
            amount=request.amount,
            currency=request.currency,
            reference_id=request.provider_reference,
            description=description,
        )

        return created_attempt, invoice

    def get_payment_attempts_for_invoice(self, invoice_id: int) -> List[PaymentAttempt]:
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise EntityNotFoundError(f"Invoice #{invoice_id} not found.")
        return self.payment_attempt_repo.get_by_invoice_id(invoice_id)
