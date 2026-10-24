def test_create_customer_success(client):
    """Test successful customer creation with Indian business details."""
    payload = {
        "name": "Aarav Sharma",
        "email": "aarav.sharma@tatadigital.in",
        "company_name": "Tata Digital Limited"
    }
    response = client.post("/customers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Aarav Sharma"
    assert data["email"] == "aarav.sharma@tatadigital.in"
    assert data["company_name"] == "Tata Digital Limited"
    assert data["status"] == "active"
    assert "id" in data


def test_customer_email_must_be_unique(client):
    """Ensure duplicate customer registration attempts with the same email are rejected."""
    payload = {
        "name": "Priya Patel",
        "email": "priya.patel@zerodhatech.in",
        "company_name": "Zerodha Broking Limited"
    }
    # First customer creation succeeds
    res1 = client.post("/customers", json=payload)
    assert res1.status_code == 201

    # Second customer with the same email must fail
    res2 = client.post("/customers", json=payload)
    assert res2.status_code == 409
    data = res2.json()
    assert "already exists" in data["detail"].lower()


def test_get_customer_and_not_found(client):
    """Test retrieving existing customer and handling not found."""
    # Create customer
    res = client.post("/customers", json={
        "name": "Rohan Verma",
        "email": "rohan.verma@swiggy.in",
        "company_name": "Bundl Technologies Pvt Ltd"
    })
    cust_id = res.json()["id"]

    # Fetch customer
    get_res = client.get(f"/customers/{cust_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Rohan Verma"
    assert get_res.json()["company_name"] == "Bundl Technologies Pvt Ltd"

    # Non-existent customer
    nf_res = client.get("/customers/999999")
    assert nf_res.status_code == 404
