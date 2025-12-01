from dataclasses import dataclass
from pydantic import BaseModel
from application.interfaces.file import FileRepository
from application.interfaces.identity_provider import IdentityProvider

class DeleteFileRequest(BaseModel):
    file_id: int

class DeleteFileInteractor:
    def __init__(self, file_repository: FileRepository ,identity_provider: IdentityProvider) -> None:
        self._file_repository = file_repository
        self._identity_provider = identity_provider


    async def __call__(self, request: DeleteFileRequest) -> None:
        await self._identity_provider.require_authenticated_user()
        await self._file_repository.delete(request.file_id)
        await self._file_repository.commit()