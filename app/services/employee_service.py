from math import ceil

from sqlalchemy.orm import Session

from app.exceptions.domain import DuplicateEmailException, EmployeeNotFoundException
from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeRequest, EmployeeResponse
from app.schemas.pagination import PaginatedResponse


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = EmployeeRepository(db)

    def create(self, request: EmployeeRequest) -> EmployeeResponse:
        if self.repository.exists_by_email(request.email):
            raise DuplicateEmailException(request.email)
        entity = Employee(**request.model_dump())
        saved = self.repository.save(entity)
        self.db.commit()
        self.db.refresh(saved)
        return EmployeeResponse.model_validate(saved)

    def find_by_id(self, employee_id: int) -> EmployeeResponse:
        entity = self.repository.find_by_id(employee_id)
        if entity is None:
            raise EmployeeNotFoundException(employee_id)
        return EmployeeResponse.model_validate(entity)

    def find_all(
        self, page: int, size: int, sort_by: str, direction: str
    ) -> PaginatedResponse[EmployeeResponse]:
        descending = direction.lower() == "desc"
        items, total = self.repository.find_all(page, size, sort_by, descending)
        total_pages = ceil(total / size) if size else 0
        return PaginatedResponse[EmployeeResponse](
            response=[EmployeeResponse.model_validate(e) for e in items],
            total_elements=total,
            total_pages=total_pages,
            current_page=page,
            page_size=size,
        )

    def update(self, employee_id: int, request: EmployeeRequest) -> EmployeeResponse:
        entity = self.repository.find_by_id(employee_id)
        if entity is None:
            raise EmployeeNotFoundException(employee_id)

        if entity.email != request.email and self.repository.exists_by_email(
            request.email
        ):
            raise DuplicateEmailException(request.email)

        for field, value in request.model_dump().items():
            setattr(entity, field, value)

        saved = self.repository.save(entity)
        self.db.commit()
        self.db.refresh(saved)
        return EmployeeResponse.model_validate(saved)

    def delete(self, employee_id: int) -> None:
        entity = self.repository.find_by_id(employee_id)
        if entity is None:
            raise EmployeeNotFoundException(employee_id)
        self.repository.delete(entity)
        self.db.commit()
