from datetime import datetime, UTC
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from application.exceptions import NotFoundError
from application.interfaces.file import FileRepository
from domain.entities.file import File
from domain.entities.user import User
from domain.constants import SINGLE_RESULT_LIMIT, SINGLE_RESULT_OFFSET
from infrastructure.database.tables.file import files_table
from infrastructure.database.tables.user import users_table


class SQLFileRepository(FileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, file: File) -> File:
        self._session.add(file)
        await self._session.flush()
        return file

    async def get_by_s3_key(self, s3_key: str) -> File | None:
        stmt = (
            select(File)
            .where(files_table.c.s3_key == s3_key)
            .where(files_table.c.deleted_at.is_(None))
            .limit(SINGLE_RESULT_LIMIT)
            .offset(SINGLE_RESULT_OFFSET)
            .order_by(files_table.c.id.desc())
        )
        return await self._session.scalar(stmt)

    async def get_by_id(self, file_id: int) -> File | None:
        stmt = (
            select(File)
            .where(files_table.c.id == file_id)
            .where(files_table.c.deleted_at.is_(None))
        )
        return await self._session.scalar(stmt)

    async def commit(self):
        await self._session.commit()

    async def get_files(self, page: int, page_size: int) -> list[tuple[File, User | None]]:
        stmt = (
            select(File, User)
            .outerjoin(User, files_table.c.user_id == users_table.c.id)
            .where(files_table.c.deleted_at.is_(None))
            .order_by(files_table.c.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [(file, user) for file, user in result.all()]

    async def count_files(self) -> int:
        """Count total files excluding soft deleted"""
        stmt = (
            select(func.count())
            .select_from(files_table)
            .where(files_table.c.deleted_at.is_(None))
        )
        result = await self._session.scalar(stmt)
        return result or 0

    async def delete(self, file_id: int) -> None:
        file = await self.get_by_id(file_id)
        if not file:
            raise NotFoundError(f"File with id {file_id} not found")
        
        # Soft delete
        file.deleted_at = datetime.now(UTC)
        await self._session.flush()