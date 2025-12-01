from pydantic import BaseModel, Field
from application.helpers.pagination import PaginatedResponse
from application.interfaces.file import FileRepository
from domain.entities.file import File
from domain.entities.user import User, UserId
from domain.constants import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    MIN_PAGE,
    MIN_PAGE_SIZE,
    MAX_PAGE_SIZE,
)


class ListFileRequest(BaseModel):
    page: int = Field(
        default=DEFAULT_PAGE,
        ge=MIN_PAGE,
        description="Page number (starts from 1)"
    )
    page_size: int = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=MIN_PAGE_SIZE,
        le=MAX_PAGE_SIZE,
        description=f"Items per page (max {MAX_PAGE_SIZE})"
    )


class FileDTO(BaseModel):
    id: int | None
    user_id: UserId | None
    s3_key: str | None
    user: User | None


class ListFileResponse(PaginatedResponse[FileDTO]):
    pass


class ListFileInteractor:
    def __init__(self, file_repository: FileRepository) -> None:
        self._file_repository = file_repository

    async def __call__(self, data: ListFileRequest) -> ListFileResponse:
        files_with_users = await self._file_repository.get_files(data.page, data.page_size)
        total = await self._file_repository.count_files()
        
        items = [
            FileDTO(id=file.id, user_id=file.user_id, s3_key=file.s3_key ,user= user)
            for file, user in files_with_users
        ]
        
        return ListFileResponse.create(
            items=items,
            page=data.page,
            page_size=data.page_size,
            total=total,
        )