import pytest

from app.exceptions.domain import DuplicateEmailException, EmployeeNotFoundException
from app.models.department import Department
from app.schemas.employee import EmployeeRequest
from app.services.employee_service import EmployeeService


@pytest.fixture
def request_payload() -> EmployeeRequest:
    return EmployeeRequest(
        first_name="Alice",
        last_name="Johnson",
        email="alice@example.com",
        phone_number="+1-555-0101",
        department=Department.FINANCE,
    )


def test_create_then_find_by_id(db_session, request_payload):
    service = EmployeeService(db_session)

    created = service.create(request_payload)
    found = service.find_by_id(created.employee_id)

    assert found.email == request_payload.email
    assert found.department == Department.FINANCE


def test_create_duplicate_email_raises(db_session, request_payload):
    service = EmployeeService(db_session)
    service.create(request_payload)

    with pytest.raises(DuplicateEmailException):
        service.create(request_payload)


def test_find_by_id_unknown_raises(db_session):
    service = EmployeeService(db_session)

    with pytest.raises(EmployeeNotFoundException):
        service.find_by_id(9999)


def test_update_changes_fields(db_session, request_payload):
    service = EmployeeService(db_session)
    created = service.create(request_payload)

    new_request = request_payload.model_copy(update={"first_name": "Alicia"})
    updated = service.update(created.employee_id, new_request)

    assert updated.first_name == "Alicia"
    assert updated.employee_id == created.employee_id


def test_delete_removes_employee(db_session, request_payload):
    service = EmployeeService(db_session)
    created = service.create(request_payload)

    service.delete(created.employee_id)

    with pytest.raises(EmployeeNotFoundException):
        service.find_by_id(created.employee_id)
