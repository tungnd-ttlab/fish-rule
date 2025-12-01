from dataclasses import dataclass

from pydantic import BaseModel, HttpUrl
from application.exceptions import AuthenticationRequiredError
from domain.entities.file import File

from application.interfaces.file import FileRepository
from application.interfaces.identity_provider import IdentityProvider


@dataclass
class PostFileRequest(BaseModel):
    s3_key: HttpUrl


@dataclass
class PostFileResponse:
    message: str

class PostFileInteractor:
    def __init__(
        self,
        file_repository: FileRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._file_repository = file_repository
        self._identity_provider = identity_provider

    async def __call__(self, data: PostFileRequest) -> PostFileResponse:
        # Get user_id if authenticated, otherwise None
        user_id = None
        try:
            if await self._identity_provider.is_authenticated():
                user_id = await self._identity_provider.get_current_user_id()
            else:
                raise AuthenticationRequiredError("User is not authenticated")
        except Exception or not user_id: 
            raise AuthenticationRequiredError("User is not authenticated")
        file = File(id=None, user_id=user_id, s3_key=data.s3_key)
        
        await self._file_repository.create(file)
        await self._file_repository.commit()
        return PostFileResponse(message="File posted successfully")