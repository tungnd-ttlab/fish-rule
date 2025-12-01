from datetime import datetime, UTC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.exceptions import ApplicationError, NotFoundError
from application.interfaces.file import FileRepository
from domain.entities.file import File
from domain.entities.user import User
from infrastructure.database.tables.file import files_table
from infrastructure.database.tables.user import users_table
from application.interfaces.base_repository import BaseRepository
class SQLFileRepository(FileRepository ,BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        BaseRepository.__init__(self, model=File, session=session)

    async def create(self, file: File) -> File:
        await self.save({
            "user_id": file.user_id,
            "s3_key": file.s3_key,
        })

        return file

    async def get_by_s3_key(self, s3_key: str) -> File | None:
        stmt = select(File).where(files_table.c.s3_key == s3_key).limit(1).offset(0).order_by(files_table.c.id.desc())
        return await self._session.scalar(stmt)

    async def get_by_id(self, file_id: int) -> File | None:
        return await self.get(file_id)

    async def get_files(self, page: int, page_size: int) -> list[tuple[File , User]]:
        stmt = select(File, User).join(User, files_table.c.user_id == users_table.c.id).order_by(files_table.c.id.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(stmt)
        return [(file, user) for file, user in result.all()]

    async def delete(self, file_id: int) -> None:
        file = await self.get_by_id(file_id)

        if not file:
            raise NotFoundError(f"File with id {file_id} not found")

        await self.soft_delete(file_id)

    
    async def commit(self):
        await self._session.commit()