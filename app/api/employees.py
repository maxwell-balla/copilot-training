import logging

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.employee import EmployeeRequest, EmployeeResponse
from app.schemas.pagination import PaginatedResponse
from app.services.employee_service import EmployeeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/employees", tags=["employees"])


def get_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
def create(
    request: EmployeeRequest,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    logger.info("Incoming request: create employee email=%s", request.email)
    return service.create(request)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def find_by_id(
    employee_id: int,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    logger.info("Incoming request: find employee by id=%s", employee_id)
    return service.find_by_id(employee_id)


@router.get("", response_model=PaginatedResponse[EmployeeResponse])
def find_all(
    page: int = Query(default=0, ge=0),
    size: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="created_at", alias="sortBy"),
    direction: str = Query(default="asc", pattern="^(?i)(asc|desc)$"),
    service: EmployeeService = Depends(get_service),
) -> PaginatedResponse[EmployeeResponse]:
    logger.info(
        "Incoming request: list employees page=%s size=%s sortBy=%s direction=%s",
        page, size, sort_by, direction,
    )
    return service.find_all(page, size, sort_by, direction)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update(
    employee_id: int,
    request: EmployeeRequest,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    logger.info(
        "Incoming request: update employee id=%s email=%s", employee_id, request.email
    )
    return service.update(employee_id, request)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    employee_id: int,
    service: EmployeeService = Depends(get_service),
) -> Response:
    logger.info("Incoming request: delete employee id=%s", employee_id)
    service.delete(employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
