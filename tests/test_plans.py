from decimal import Decimal


def test_create_plan_success(client):
    """Test successful plan creation with INR currency."""
    payload = {
        "name": "Pro Monthly INR",
        "description": "Professional billing tier for Indian startups and SaaS companies",
        "billing_cycle": "monthly",
        "price": 1499.00,
        "currency": "INR"
    }
    response = client.post("/plans", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Pro Monthly INR"
    assert data["billing_cycle"] == "monthly"
    assert float(data["price"]) == 1499.00
    assert data["status"] == "active"
    assert data["currency"] == "INR"
    assert "id" in data


def test_create_plan_price_must_be_greater_than_zero(client):
    """Ensure plan price validation rejects zero or negative amounts."""
    # Test zero price
    payload_zero = {
        "name": "Freebie Plan INR",
        "description": "Attempting zero price in INR",
        "billing_cycle": "monthly",
        "price": 0.0,
        "currency": "INR"
    }
    response_zero = client.post("/plans", json=payload_zero)
    assert response_zero.status_code in [422, 400]

    # Test negative price
    payload_negative = {
        "name": "Negative Plan INR",
        "description": "Attempting negative price in INR",
        "billing_cycle": "monthly",
        "price": -100.0,
        "currency": "INR"
    }
    response_negative = client.post("/plans", json=payload_negative)
    assert response_negative.status_code in [422, 400]


def test_list_and_update_plan(client):
    """Test listing plans and updating / deactivating an INR plan."""
    # Create plan
    res = client.post("/plans", json={
        "name": "Starter Plan INR",
        "billing_cycle": "monthly",
        "price": 499.00,
        "currency": "INR"
    })
    plan_id = res.json()["id"]

    # List plans
    list_res = client.get("/plans")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Update plan price and deactivate
    patch_res = client.patch(f"/plans/{plan_id}", json={
        "price": 599.00,
        "status": "inactive"
    })
    assert patch_res.status_code == 200
    updated_data = patch_res.json()
    assert float(updated_data["price"]) == 599.00
    assert updated_data["status"] == "inactive"
