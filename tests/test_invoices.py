def test_generate_invoice_amount_due_from_plan_price(client):
    """Verify that invoice amount_due snapshots current plan pricing in INR and logs ledger event."""
    # 1. Create plan with price ₹4,999.00 INR
    p_res = client.post("/plans", json={
        "name": "Enterprise Cloud INR",
        "billing_cycle": "monthly",
        "price": 4999.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    # 2. Create Indian customer and subscription
    c_res = client.post("/customers", json={
        "name": "Ananya Sen",
        "email": "ananya.sen@tatacapital.in",
        "company_name": "Tata Capital Financial Services"
    })
    customer_id = c_res.json()["id"]

    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    sub_id = sub_res.json()["id"]

    # 3. Generate invoice
    inv_res = client.post("/invoices/generate", json={
        "subscription_id": sub_id
    })
    assert inv_res.status_code == 201
    inv_data = inv_res.json()
    assert float(inv_data["amount_due"]) == 4999.00
    assert float(inv_data["amount_paid"]) == 0.00
    assert inv_data["currency"] == "INR"
    assert inv_data["status"] == "issued"
    assert inv_data["subscription_id"] == sub_id
    assert inv_data["customer_id"] == customer_id

    # 4. Verify that invoice_created ledger entry was created
    ledger_res = client.get(f"/customers/{customer_id}/ledger")
    assert ledger_res.status_code == 200
    ledger_entries = ledger_res.json()
    assert len(ledger_entries) == 1
    assert ledger_entries[0]["entry_type"] == "invoice_created"
    assert float(ledger_entries[0]["amount"]) == 4999.00
    assert ledger_entries[0]["currency"] == "INR"
    assert ledger_entries[0]["reference_id"] == f"INV-{inv_data['id']}"


def test_cannot_generate_invoice_for_cancelled_subscription(client):
    """Test that invoice cannot be generated for a cancelled subscription."""
    p_res = client.post("/plans", json={
        "name": "Standard Business INR",
        "billing_cycle": "monthly",
        "price": 1299.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    c_res = client.post("/customers", json={
        "name": "Deepak Chopra",
        "email": "deepak.chopra@wipro.in",
        "company_name": "Wipro Enterprises"
    })
    customer_id = c_res.json()["id"]

    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    sub_id = sub_res.json()["id"]

    # Cancel subscription
    client.patch(f"/subscriptions/{sub_id}/cancel")

    # Attempt to generate invoice
    inv_res = client.post("/invoices/generate", json={"subscription_id": sub_id})
    assert inv_res.status_code == 422
    assert "cannot generate invoice" in inv_res.json()["detail"].lower()
