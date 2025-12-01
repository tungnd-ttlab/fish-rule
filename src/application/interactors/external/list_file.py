from dataclasses import dataclass
from pydantic import BaseModel, HttpUrl
from application.interfaces.file import FileRepository
from domain.entities.file import File
from domain.entities.user import User


@dataclass
class ListFileRequest(BaseModel):
    page: int = 1
    page_size: int = 10


class FileDTO(BaseModel):
    file: File 
    user: User

class ListFileResponse(BaseModel):
    files: list[FileDTO]

class ListFileInteractor:
    def __init__(self, file_repository: FileRepository)-> None:
        self._file_repository = file_repository

    async def __call__(self, data: ListFileRequest) -> ListFileResponse:
        files_with_users = await self._file_repository.get_files(data.page, data.page_size)
        return ListFileResponse(
            files=[
                FileDTO(file=file, user=user) 
                for file, user in files_with_users
            ]
        )