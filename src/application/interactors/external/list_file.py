from dataclasses import dataclass
from pydantic import BaseModel, HttpUrl
from application.interfaces.file import FileRepository
from domain.entities.file import File


@dataclass
class ListFileRequest(BaseModel):
    page: int
    page_size: int

@dataclass
class ListFileResponse(BaseModel):
    files: list[File]

class ListFileInteractor:
    def __init__(self, file_repository: FileRepository)-> None:
        self._file_repository = file_repository

    async def __call__(self, data: ListFileRequest) -> ListFileResponse:
        files = await self._file_repository.get_files(data.page, data.page_size)
        return ListFileResponse(files=files)