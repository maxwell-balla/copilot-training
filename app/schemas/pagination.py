from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    response: list[T]
    total_elements: int
    total_pages: int
    current_page: int
    page_size: int
