# SubLedger - SaaS Subscription & Billing System

A robust, modular SaaS subscription and billing backend built with **Python 3.12**, **FastAPI**, and **SQLAlchemy 2.0**. SubLedger is designed from the ground up according to **Low-Level Design (LLD)** best practices, **SOLID principles**, the **Repository Pattern**, the **Service Layer Pattern**, and an **append-only Financial Ledger**.

---

## 1. Key Architectural Features

- **Layered Architecture**: Strict separation of concerns between:
  - `routes` (`app/api/v1/endpoints/`)
  - `services` (`app/services/`)
  - `repositories` (`app/repositories/`)
  - `models` (`app/models/`)
  - `schemas` (`app/schemas/`)
  - `database / session management` (`app/db/`)
  - `configuration` (`app/config.py`)
- **Repository Pattern**: All database read/write queries are isolated into specialized repository classes.
- **Service Layer**: All domain rules, validations, calculations, and multi-entity workflows are encapsulated inside service classes.
- **Dependency Injection**: Repositories, database sessions, and services are decoupled and injected using FastAPI's dependency injection system (`app/api/deps.py`).
- **Append-Only Financial Ledger**: Immutable audit log of all financial events (`invoice_created`, `payment_success`, `payment_failure`) traceable via `reference_id`.
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **100% Passing Test Suite**: 16 comprehensive unit & integration tests covering all critical business rules.

---

## 2. Project Structure

```text
SubLedger - SaaS Subscription & Billing System/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Application entry point, CORS & exception handlers
│   ├── config.py                   # Pydantic Settings & environment config
│   ├── exceptions.py               # Custom domain exceptions (EntityNotFound, BusinessRuleViolation, etc.)
│   ├── db/
│   │   ├── __init__.py             # Exports Base, SessionLocal, engine, get_db
│   │   ├── base.py                 # Declarative Base
│   │   └── session.py              # Engine and SessionLocal generator
│   ├── models/                     # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── plan.py                 # Plan model
│   │   ├── customer.py             # Customer model
│   │   ├── subscription.py         # Subscription model
│   │   ├── invoice.py              # Invoice model (matches assignment skeleton)
│   │   ├── payment_attempt.py      # PaymentAttempt model
│   │   └── ledger_entry.py         # Append-only LedgerEntry model
│   ├── schemas/                    # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── plan.py
│   │   ├── customer.py
│   │   ├── subscription.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   └── ledger.py
│   ├── repositories/               # Repository Data Access Layer
│   │   ├── __init__.py
│   │   ├── base.py                 # Generic BaseRepository
│   │   ├── plan_repository.py
│   │   ├── customer_repository.py
│   │   ├── subscription_repository.py
│   │   ├── invoice_repository.py
│   │   ├── payment_attempt_repository.py
│   │   └── ledger_repository.py    # Append-only repository (no updates/deletions)
│   ├── services/                   # Service Business Logic Layer
│   │   ├── __init__.py
│   │   ├── plan_service.py
│   │   ├── customer_service.py
│   │   ├── subscription_service.py
│   │   ├── invoice_service.py
│   │   ├── payment_service.py
│   │   └── ledger_service.py
│   └── api/                        # Route Controllers
│       ├── __init__.py
│       ├── deps.py                 # Dependency injection factory
│       └── v1/
│           ├── __init__.py
│           ├── api.py              # Router registration
│           └── endpoints/
│               ├── __init__.py
│               ├── plans.py        # /plans endpoints
│               ├── customers.py    # /customers and /customers/{id}/ledger
│               ├── subscriptions.py# /subscriptions and cancellation
│               ├── invoices.py     # /invoices/generate and /invoices/{id}
│               └── payments.py     # /payments/record
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # In-memory test DB fixtures
│   ├── test_plans.py               # Tests for plan rules & price > 0
│   ├── test_customers.py           # Tests for unique email & profile
│   ├── test_subscriptions.py       # Tests for plan active check & no duplicates
│   ├── test_invoices.py            # Tests for price snapshot & invoice creation
│   ├── test_payments.py            # Tests for partial/full payment, failed payment, and limits
│   └── test_ledger.py              # Tests for append-only traceability
├── Dockerfile                      # Production container image
├── docker-compose.yml              # Local container deployment
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── DESIGN.md                       # Comprehensive Low-Level Design document
└── README.md                       # Documentation & run instructions
```

---

## 3. Quick Start & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git (optional)
- Docker & Docker Compose (optional for container execution)

### Option A: Local Python Setup

1. **Clone or navigate to the repository directory**:
   ```bash
   cd "SubLedger - SaaS Subscription & Billing System"
   ```

2. **Create and activate a virtual environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**:
   ```bash
   cp .env.example .env
   ```

5. **Start the API server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access Interactive API Docs**:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option B: Docker Setup

Build and run using Docker Compose:

```bash
docker compose up --build -d
```

The server will be available at [http://localhost:8000](http://localhost:8000).

---

## 4. Running the Automated Test Suite

SubLedger includes a comprehensive test suite executed against an isolated in-memory SQLite database:

```bash
# Run pytest with detailed verbose output
pytest -v

# Or run with Python directly
python -m pytest -v
```

### Test Results
```text
tests/test_customers.py::test_create_customer_success PASSED             [  6%]
tests/test_customers.py::test_customer_email_must_be_unique PASSED       [ 12%]
tests/test_customers.py::test_get_customer_and_not_found PASSED          [ 18%]
tests/test_invoices.py::test_generate_invoice_amount_due_from_plan_price PASSED [ 25%]
tests/test_invoices.py::test_cannot_generate_invoice_for_cancelled_subscription PASSED [ 31%]
tests/test_ledger.py::test_ledger_append_only_and_traceability PASSED    [ 37%]
tests/test_payments.py::test_partial_and_full_payment_status_transitions PASSED [ 43%]
tests/test_payments.py::test_payment_cannot_exceed_remaining_unpaid_amount PASSED [ 50%]
tests/test_payments.py::test_failed_payment_does_not_increase_amount_paid PASSED [ 56%]
tests/test_plans.py::test_create_plan_success PASSED                     [ 62%]
tests/test_plans.py::test_create_plan_price_must_be_greater_than_zero PASSED [ 68%]
tests/test_plans.py::test_list_and_update_plan PASSED                    [ 75%]
tests/test_subscriptions.py::test_create_subscription_success PASSED     [ 81%]
tests/test_subscriptions.py::test_cannot_create_subscription_for_inactive_plan PASSED [ 87%]
tests/test_subscriptions.py::test_no_duplicate_active_subscription_to_same_plan PASSED [ 93%]
tests/test_subscriptions.py::test_cancel_subscription PASSED             [100%]

======================= 16 passed in 0.85s =======================
```

---

## 5. API Reference & Endpoints

All endpoints are accessible both directly at root (`/plans`) and under `/api/v1` (`/api/v1/plans`).

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `POST` | `/plans` | Create a subscription plan | `201 Created` |
| `GET` | `/plans` | List subscription plans | `200 OK` |
| `PATCH` | `/plans/{plan_id}` | Update/deactivate a plan | `200 OK` |
| `POST` | `/customers` | Create a customer | `201 Created` |
| `GET` | `/customers` | List customers | `200 OK` |
| `GET` | `/customers/{customer_id}` | Fetch customer details | `200 OK` |
| `POST` | `/subscriptions` | Create a subscription | `201 Created` |
| `GET` | `/subscriptions` | List subscriptions | `200 OK` |
| `PATCH` | `/subscriptions/{subscription_id}/cancel` | Cancel a subscription | `200 OK` |
| `POST` | `/invoices/generate` | Generate invoice for a subscription | `201 Created` |
| `GET` | `/invoices/{invoice_id}` | Fetch invoice details | `200 OK` |
| `POST` | `/payments/record` | Record a payment attempt | `201 Created` |
| `GET` | `/customers/{customer_id}/ledger` | Fetch customer ledger history | `200 OK` |

---

## 6. End-to-End Walkthrough & Example Payloads

### Step 1: Create a Plan
```bash
curl -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Growth Tier",
    "description": "Unlimited billing and ledger audit trails",
    "billing_cycle": "monthly",
    "price": 49.00,
    "currency": "USD"
  }'
```

### Step 2: Create a Customer
```bash
curl -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Connor",
    "email": "sarah.connor@sky.net",
    "company_name": "Cyberdyne Systems"
  }'
```

### Step 3: Create a Subscription
```bash
curl -X POST http://localhost:8000/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "plan_id": 1
  }'
```

### Step 4: Generate an Invoice
```bash
curl -X POST http://localhost:8000/invoices/generate \
  -H "Content-Type: application/json" \
  -d '{
    "subscription_id": 1
  }'
```
*Note: This automatically logs an `invoice_created` entry in the customer's financial ledger.*

### Step 5: Record a Payment Attempt (Partial or Full)
```bash
curl -X POST http://localhost:8000/payments/record \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": 1,
    "amount": 25.00,
    "currency": "USD",
    "status": "success",
    "provider_reference": "TXN_STRIPE_123456"
  }'
```
*Result: Invoice status moves to `partially_paid` ($25 paid of $49 due). A `payment_success` entry is appended to the ledger.*

### Step 6: View Customer Ledger History
```bash
curl -X GET http://localhost:8000/customers/1/ledger
```
*Returns all immutable events (`invoice_created`, `payment_success`) with timestamps and external reference IDs.*

---

## 7. Assumptions & Limitations

### Assumptions
1. **Currencies**: Currencies are represented as 3-letter ISO codes (e.g. `USD`, `EUR`, `INR`). Multi-currency conversion is not performed; payments are recorded in the specified invoice currency.
2. **Billing Cycles**: Supported cycles are `"monthly"` (30 days), `"quarterly"` (90 days), and `"yearly"` (365 days).
3. **Price Stability**: Generating an invoice takes an immutable snapshot of `plan.price` at the moment of invoice generation, ensuring future plan price revisions do not alter historical invoice records.
4. **Append-Only Immutability**: Ledger records cannot be updated or deleted through any repository method or API route.

### Limitations & Out-of-Scope (as defined in brief)
1. **Payment Gateway Integration**: Payment attempts are recorded via API simulations; direct webhooks with Stripe/Razorpay are mocked through provider references.
2. **Proration & Upgrades**: Mid-cycle upgrade proration calculations are out of scope for the base version.
3. **Authentication/RBAC**: Authentication is omitted to keep the system clean and focused on billing domain logic, but can be added cleanly via FastAPI middleware.
4. **Tax Engine**: Complex multi-jurisdiction tax calculations (VAT/GST) are excluded in favor of clean base amounts.

---

## 8. License

This project was built for the Airtribe Backend Engineering Assessment.
