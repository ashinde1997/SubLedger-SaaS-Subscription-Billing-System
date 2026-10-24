def setup_invoice(client, price=1000.00):
    p_res = client.post("/plans", json={
        "name": "Standard SaaS Tier INR",
        "billing_cycle": "monthly",
        "price": price,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    c_res = client.post("/customers", json={
        "name": "Rajesh Nair",
        "email": f"rajesh.nair_{int(price)}@bajajfinserv.in",
        "company_name": "Bajaj Finserv Limited"
    })
    customer_id = c_res.json()["id"]

    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    sub_id = sub_res.json()["id"]

    inv_res = client.post("/invoices/generate", json={"subscription_id": sub_id})
    invoice_id = inv_res.json()["id"]
    return customer_id, invoice_id


def test_partial_and_full_payment_status_transitions(client):
    """Verify invoice transitions to partially_paid and paid upon progressive settlements in INR."""
    customer_id, invoice_id = setup_invoice(client, price=1000.00)

    # 1. Record partial UPI payment of ₹400
    pay1 = client.post("/payments/record", json={
        "invoice_id": invoice_id,
        "amount": 400.00,
        "currency": "INR",
        "status": "success",
        "provider_reference": "pay_razorpay_upi_01"
    })
    assert pay1.status_code == 201
    pay1_data = pay1.json()
    assert pay1_data["payment_attempt"]["status"] == "success"
    assert float(pay1_data["invoice"]["amount_paid"]) == 400.00
    assert pay1_data["invoice"]["status"] == "partially_paid"

    # 2. Record remaining NetBanking payment of ₹600
    pay2 = client.post("/payments/record", json={
        "invoice_id": invoice_id,
        "amount": 600.00,
        "currency": "INR",
        "status": "success",
        "provider_reference": "pay_hdfc_netbanking_02"
    })
    assert pay2.status_code == 201
    pay2_data = pay2.json()
    assert float(pay2_data["invoice"]["amount_paid"]) == 1000.00
    assert pay2_data["invoice"]["status"] == "paid"


def test_payment_cannot_exceed_remaining_unpaid_amount(client):
    """Verify rejection when a payment attempt exceeds the remaining balance in INR."""
    customer_id, invoice_id = setup_invoice(client, price=500.00)

    # Attempt to pay ₹600 on a ₹500 invoice
    pay_excess = client.post("/payments/record", json={
        "invoice_id": invoice_id,
        "amount": 600.00,
        "currency": "INR",
        "status": "success",
        "provider_reference": "pay_excess_fail"
    })
    assert pay_excess.status_code == 422
    assert "cannot exceed the remaining unpaid amount" in pay_excess.json()["detail"].lower()


def test_failed_payment_does_not_increase_amount_paid(client):
    """Verify that a declined UPI payment logs the attempt but does not mutate invoice balance."""
    customer_id, invoice_id = setup_invoice(client, price=800.00)

    # Record failed payment attempt
    pay_fail = client.post("/payments/record", json={
        "invoice_id": invoice_id,
        "amount": 800.00,
        "currency": "INR",
        "status": "failed",
        "provider_reference": "pay_upi_failed_mandate",
        "failure_reason": "UPI mandate approval timed out by customer bank"
    })
    assert pay_fail.status_code == 201
    pay_data = pay_fail.json()
    assert pay_data["payment_attempt"]["status"] == "failed"
    assert pay_data["payment_attempt"]["failure_reason"] == "UPI mandate approval timed out by customer bank"
    assert float(pay_data["invoice"]["amount_paid"]) == 0.00
    assert pay_data["invoice"]["status"] == "issued"

    # Verify ledger entry was created for payment_failure
    ledger_res = client.get(f"/customers/{customer_id}/ledger")
    assert ledger_res.status_code == 200
    entries = ledger_res.json()
    types = [e["entry_type"] for e in entries]
    assert "invoice_created" in types
    assert "payment_failure" in types
