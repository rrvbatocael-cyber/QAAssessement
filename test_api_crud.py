import pytest
from playwright.sync_api import APIRequestContext

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="module")
def auth_token(playwright):
    """Generates an authentication token required for mutation requests."""
    request_context = playwright.request.new_context(base_url=BASE_URL)
    
    payload = {
        "username": "admin",
        "password": "password123"
    }=
    
    response = request_context.post("/auth", json=payload)
    assert response.status == 200
    
    token = response.json().get("token")
    assert token is not None
    
    yield token
    request_context.dispose()

def test_api_booking_crud_lifecycle(playwright, auth_token):
    """Verifies the positive Create, Read, Update, and Delete flow."""
    request_context = playwright.request.new_context(base_url=BASE_URL)
    

    create_payload = {
        "firstname": "Rozellini",
        "lastname": "Batocael",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-07-01",
            "checkout": "2026-07-05"
        },
        "additionalneeds": "Extra Pillows"
    }
    
    create_response = request_context.post("/booking", json=create_payload)
    assert create_response.status == 200
    
    create_json = create_response.json()
    assert "bookingid" in create_json
    booking_id = create_json["bookingid"]
    assert create_json["booking"]["firstname"] == "Rozellini"

    # -------------------------------------------------------------------------
    # 2. READ (GET)
    # -------------------------------------------------------------------------
    read_response = request_context.get(f"/booking/{booking_id}")
    assert read_response.status == 200
    assert read_response.json()["lastname"] == "Batocael"

    # -------------------------------------------------------------------------
    # 3. UPDATE (PUT)
    # -------------------------------------------------------------------------
    update_payload = {
        "firstname": "Rozellini",
        "lastname": "Batocael",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-07-01",
            "checkout": "2026-07-05"
        },
        "additionalneeds": "Late Checkout"
    }
    
    # Restful-Booker requires authentication credentials passed inside the Cookie header
    update_response = request_context.put(
        f"/booking/{booking_id}",
        json=update_payload,
        headers={"Cookie": f"token={auth_token}"}
    )
    assert update_response.status == 200
    assert update_response.json()["firstname"] == "Rozellini"
    assert update_response.json()["additionalneeds"] == "Late Checkout"

    # -------------------------------------------------------------------------
    # 4. DELETE (DELETE)
    # -------------------------------------------------------------------------
    delete_response = request_context.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )
    # Restful-Booker returns 201 Created on a successful resource deletion
    assert delete_response.status == 201 

    # Verify resource deletion via an immediate GET check
    verify_deleted = request_context.get(f"/booking/{booking_id}")
    assert verify_deleted.status == 404
    
    request_context.dispose()

def test_api_read_negative_invalid_id(playwright):
    """5. NEGATIVE CASE: Attempt to read an ID that does not exist."""
    request_context = playwright.request.new_context(base_url=BASE_URL)
    
    invalid_id = 999999
    response = request_context.get(f"/booking/{invalid_id}")
    
    # Asserting that the endpoint rejects the transaction with a 404 Not Found
    assert response.status == 404
    
    request_context.dispose()