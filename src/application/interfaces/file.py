from abc import abstractmethod
from typing import Protocol
from domain.entities.file import File
from domain.entities.user import User


class FileRepository(Protocol):
    @abstractmethod
    async def delete(self, file_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, file: File) -> File:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, file_id: int) -> File | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_s3_key(self, s3_key: str) -> File | None:
        raise NotImplementedError
        
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_files(self, page: int, page_size: int) -> list[tuple[File , User]]:
        raise NotImplementedError