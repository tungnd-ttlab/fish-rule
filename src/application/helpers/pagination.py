from typing import Generic, TypeVar, Self
from pydantic import BaseModel, Field
from domain.constants import (
    MIN_PAGE,
    MIN_PAGE_SIZE,
    MAX_PAGE_SIZE,
)

T = TypeVar('T')


class PaginationMeta(BaseModel):
    """Metadata about pagination"""
    page: int = Field(ge=MIN_PAGE, description="Current page number")
    page_size: int = Field(ge=MIN_PAGE_SIZE, le=MAX_PAGE_SIZE, description="Items per page")
    total: int = Field(ge=0, description="Total number of items")
    total_pages: int = Field(ge=0, description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: list[T] = Field(description="List of items in current page")
    meta: PaginationMeta = Field(description="Pagination metadata")
    
    @classmethod
    def create(
        cls: type[Self],
        items: list[T],
        page: int,
        page_size: int,
        total: int,
    ) -> Self:
        """Factory method to create paginated response"""
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        return cls(
            items=items,
            meta=PaginationMeta(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            )
        )

