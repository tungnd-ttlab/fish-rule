from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from application.interfaces.file import FileRepository
from domain.entities.file import File
from infrastructure.database.tables.file import files_table


class SQLFileRepository(FileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, file: File) -> File:
        self._session.add(file)
        await self._session.flush()
        return file

    async def get_by_s3_key(self, s3_key: str) -> File | None:
        stmt = select(File).where(files_table.c.s3_key == s3_key).limit(1).offset(0).order_by(files_table.c.id.desc())
        return await self._session.scalar(stmt)

    async def get_by_id(self, file_id: int) -> File | None:
        return await self._session.get(File, file_id)

    async def commit(self):
        await self._session.commit()

    async def get_files(self, page: int, page_size: int) -> list[File]:
        stmt = select(File).order_by(files_table.c.id.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(stmt)
        return list(result.scalars())