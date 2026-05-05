from enum import Enum


class Department(str, Enum):
    HR = "HR"
    IT = "IT"
    FINANCE = "FINANCE"
    OPERATIONS = "OPERATIONS"
    MARKETING = "MARKETING"
    LEGAL = "LEGAL"
