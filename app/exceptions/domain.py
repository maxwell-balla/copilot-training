class EmployeeNotFoundException(Exception):
    def __init__(self, employee_id: int) -> None:
        super().__init__(f"Employee not found with id: {employee_id}")
        self.employee_id = employee_id


class DuplicateEmailException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"An employee with email '{email}' already exists")
        self.email = email
