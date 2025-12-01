from dataclasses import dataclass

from pydantic import BaseModel, HttpUrl
from domain.entities.file import File

from application.interfaces.file import FileRepository


@dataclass
class PostFileRequest(BaseModel):
    s3_key: HttpUrl


@dataclass
class PostFileResponse:
    message: str

class PostFileInteractor:
    def __init__(self, file_repository: FileRepository)-> None:
        self._file_repository = file_repository

    async def __call__(self, data: PostFileRequest) -> PostFileResponse:
        file = File(id=None, s3_key=data.s3_key)
        await self._file_repository.create(file)
        await self._file_repository.commit()
        return PostFileResponse(message="File posted successfully")