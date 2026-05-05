from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.department import Department


class EmployeeRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    phone_number: str = Field(min_length=1)
    department: Department


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_id: int
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    department: Department
    created_at: datetime
