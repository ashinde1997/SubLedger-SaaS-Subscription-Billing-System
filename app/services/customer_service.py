from typing import List
from app.exceptions import EntityNotFoundError, DuplicateEntityError
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service responsible for customer registration and management."""

    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def create_customer(self, customer_in: CustomerCreate) -> Customer:
        normalized_email = customer_in.email.lower().strip()
        existing = self.customer_repo.get_by_email(normalized_email)
        if existing:
            raise DuplicateEntityError(f"Customer with email '{normalized_email}' already exists.")

        customer = Customer(
            name=customer_in.name.strip(),
            email=normalized_email,
            company_name=customer_in.company_name.strip() if customer_in.company_name else None,
            status="active",
        )
        return self.customer_repo.create(customer)

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundError(f"Customer with id {customer_id} not found.")
        return customer

    def list_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.customer_repo.get_all(skip=skip, limit=limit)

    def update_customer(self, customer_id: int, customer_in: CustomerUpdate) -> Customer:
        customer = self.get_customer(customer_id)

        update_data = customer_in.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] is not None:
            customer.name = update_data["name"].strip()
        if "company_name" in update_data:
            customer.company_name = update_data["company_name"].strip() if update_data["company_name"] else None
        if "status" in update_data and update_data["status"] is not None:
            customer.status = update_data["status"]

        return self.customer_repo.update(customer)
