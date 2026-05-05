from fastapi import status


def test_create_employee_returns_201(client, employee_payload):
    response = client.post("/api/employees", json=employee_payload)

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["employee_id"] > 0
    assert body["email"] == employee_payload["email"]
    assert body["department"] == "FINANCE"
    assert "created_at" in body


def test_create_employee_with_duplicate_email_returns_409(client, employee_payload):
    client.post("/api/employees", json=employee_payload)

    response = client.post("/api/employees", json=employee_payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


def test_create_employee_with_invalid_email_returns_400(client, employee_payload):
    employee_payload["email"] = "not-an-email"

    response = client.post("/api/employees", json=employee_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["title"] == "Bad Request"
    assert "email" in response.json()["errors"]


def test_get_employee_by_id_returns_200(client, employee_payload):
    created = client.post("/api/employees", json=employee_payload).json()

    response = client.get(f"/api/employees/{created['employee_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == employee_payload["email"]


def test_get_employee_unknown_id_returns_404(client):
    response = client.get("/api/employees/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_list_employees_paginated(client, employee_payload):
    for i in range(3):
        payload = {**employee_payload, "email": f"user{i}@example.com"}
        client.post("/api/employees", json=payload)

    response = client.get("/api/employees", params={"page": 0, "size": 2})

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["total_elements"] == 3
    assert body["total_pages"] == 2
    assert body["current_page"] == 0
    assert body["page_size"] == 2
    assert len(body["response"]) == 2


def test_update_employee(client, employee_payload):
    created = client.post("/api/employees", json=employee_payload).json()
    updated = {**employee_payload, "first_name": "Alicia", "department": "IT"}

    response = client.put(f"/api/employees/{created['employee_id']}", json=updated)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["first_name"] == "Alicia"
    assert body["department"] == "IT"


def test_delete_employee_returns_204(client, employee_payload):
    created = client.post("/api/employees", json=employee_payload).json()

    response = client.delete(f"/api/employees/{created['employee_id']}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/api/employees/{created['employee_id']}").status_code == 404
