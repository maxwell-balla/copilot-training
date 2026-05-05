from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum as SAEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.department import Department


class Employee(Base):
    __tablename__ = "t_employee"

    employee_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer(), "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    department: Mapped[Department] = mapped_column(
        SAEnum(Department, native_enum=False, length=50), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
