def test_ledger_append_only_and_traceability(client):
    """Verify that ledger logs an append-only audit trail in INR with traceable reference IDs."""
    # Create plan, Indian customer, subscription, invoice, and payments
    p_res = client.post("/plans", json={
        "name": "Audit Tier INR",
        "billing_cycle": "monthly",
        "price": 750.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    c_res = client.post("/customers", json={
        "name": "Aditi Rao",
        "email": "aditi.rao@infosys.in",
        "company_name": "Infosys Limited"
    })
    customer_id = c_res.json()["id"]

    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    sub_id = sub_res.json()["id"]

    # 1. Invoice generated -> Event 1: invoice_created
    inv_res = client.post("/invoices/generate", json={"subscription_id": sub_id})
    invoice_id = inv_res.json()["id"]

    # 2. Failed payment -> Event 2: payment_failure
    client.post("/payments/record", json={
        "invoice_id": invoice_id,
        "amount": 750.00,
        "currency": "INR",
        "status": "failed",
        "provider_reference": "pay_razorpay_failed_mandate",
        "failure_reason": "Debit card international limit or OTP timeout"
    })

    # 3. Successful payment -> Event 3: payment_success
    client.post("/payments/record", json={
        "invoice_id": invoice_id,
        "amount": 750.00,
        "currency": "INR",
        "status": "success",
        "provider_reference": "pay_razorpay_upi_success_9988"
    })

    # Fetch customer ledger history
    ledger_res = client.get(f"/customers/{customer_id}/ledger")
    assert ledger_res.status_code == 200
    entries = ledger_res.json()

    # Verify append-only sequence
    assert len(entries) == 3
    assert entries[0]["entry_type"] == "invoice_created"
    assert entries[0]["reference_id"] == f"INV-{invoice_id}"
    assert float(entries[0]["amount"]) == 750.00
    assert entries[0]["currency"] == "INR"

    assert entries[1]["entry_type"] == "payment_failure"
    assert entries[1]["reference_id"] == "pay_razorpay_failed_mandate"
    assert entries[1]["currency"] == "INR"

    assert entries[2]["entry_type"] == "payment_success"
    assert entries[2]["reference_id"] == "pay_razorpay_upi_success_9988"
    assert float(entries[2]["amount"]) == 750.00
    assert entries[2]["currency"] == "INR"
