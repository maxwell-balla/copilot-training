from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        self.db.refresh(employee)
        return employee

    def find_by_id(self, employee_id: int) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def exists_by_id(self, employee_id: int) -> bool:
        return self.find_by_id(employee_id) is not None

    def exists_by_email(self, email: str) -> bool:
        stmt = select(func.count()).select_from(Employee).where(Employee.email == email)
        return self.db.execute(stmt).scalar_one() > 0

    def find_all(
        self, page: int, size: int, sort_by: str, descending: bool
    ) -> tuple[list[Employee], int]:
        sort_column = getattr(Employee, sort_by, None)
        if sort_column is None:
            sort_column = Employee.created_at
        order = sort_column.desc() if descending else sort_column.asc()

        total = self.db.execute(
            select(func.count()).select_from(Employee)
        ).scalar_one()

        stmt = select(Employee).order_by(order).limit(size).offset(page * size)
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def delete(self, employee: Employee) -> None:
        self.db.delete(employee)
