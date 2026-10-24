def test_create_subscription_success(client):
    """Test successful subscription creation for Indian SaaS customer."""
    # Create plan and customer
    p_res = client.post("/plans", json={
        "name": "Developer Pro INR",
        "billing_cycle": "monthly",
        "price": 999.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    c_res = client.post("/customers", json={
        "name": "Kavita Reddy",
        "email": "kavita.reddy@techmahindra.in",
        "company_name": "Tech Mahindra Ltd"
    })
    customer_id = c_res.json()["id"]

    # Create subscription
    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    assert sub_res.status_code == 201
    sub_data = sub_res.json()
    assert sub_data["customer_id"] == customer_id
    assert sub_data["plan_id"] == plan_id
    assert sub_data["status"] == "active"
    assert "current_period_end" in sub_data


def test_cannot_create_subscription_for_inactive_plan(client):
    """Ensure subscription creation is blocked for deactivated or archived plans."""
    # Create plan
    p_res = client.post("/plans", json={
        "name": "Legacy Startup Plan INR",
        "billing_cycle": "monthly",
        "price": 299.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    # Deactivate plan
    client.patch(f"/plans/{plan_id}", json={"status": "inactive"})

    # Create customer
    c_res = client.post("/customers", json={
        "name": "Arjun Singhania",
        "email": "arjun.singhania@singhania.in",
        "company_name": "Singhania Enterprises"
    })
    customer_id = c_res.json()["id"]

    # Attempt to subscribe
    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    assert sub_res.status_code == 422
    assert "inactive plan" in sub_res.json()["detail"].lower()


def test_no_duplicate_active_subscription_to_same_plan(client):
    """Ensure a customer cannot have multiple active subscriptions to the identical plan."""
    # Create plan and customer
    p_res = client.post("/plans", json={
        "name": "Growth Tier INR",
        "billing_cycle": "monthly",
        "price": 2499.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    c_res = client.post("/customers", json={
        "name": "Neha Gupta",
        "email": "neha.gupta@zomato.in",
        "company_name": "Zomato Limited"
    })
    customer_id = c_res.json()["id"]

    # First subscription succeeds
    sub1 = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    assert sub1.status_code == 201

    # Second active subscription to the same plan must be rejected
    sub2 = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    assert sub2.status_code == 422
    assert "already has an active subscription" in sub2.json()["detail"].lower()


def test_cancel_subscription(client):
    """Test cancelling a subscription."""
    p_res = client.post("/plans", json={
        "name": "Flexi Monthly INR",
        "billing_cycle": "monthly",
        "price": 799.00,
        "currency": "INR"
    })
    plan_id = p_res.json()["id"]

    c_res = client.post("/customers", json={
        "name": "Siddharth Rao",
        "email": "siddharth.rao@freshworks.in",
        "company_name": "Freshworks Technologies"
    })
    customer_id = c_res.json()["id"]

    sub_res = client.post("/subscriptions", json={
        "customer_id": customer_id,
        "plan_id": plan_id
    })
    sub_id = sub_res.json()["id"]

    # Cancel subscription
    cancel_res = client.patch(f"/subscriptions/{sub_id}/cancel")
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"
    assert cancel_res.json()["cancelled_at"] is not None

    # Cancelling again should return 422
    cancel_again = client.patch(f"/subscriptions/{sub_id}/cancel")
    assert cancel_again.status_code == 422
