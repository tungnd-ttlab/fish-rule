from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

class BaseRepository:
    def __init__(self, model, session: AsyncSession):
        self._model = model
        self._session = session

    async def get(self, id):
        stmt = select(self._model).where(self._model.id == id, self._model.deleted_at.is_(None))
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip=0, limit=100):
        stmt = select(self._model).where(self._model.deleted_at.is_(None)).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def save(self, obj_in: dict):
        obj = self._model(**obj_in)
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def update(self, id, obj_in: dict):
        obj = await self.get(id)
        if not obj:
            return None
        for key, value in obj_in.items():
            setattr(obj, key, value)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def soft_delete(self, id):
        obj = await self.get(id)
        if not obj:
            return None
        obj.deleted_at = datetime.utcnow()
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def commit(self):
        await self._session.commit()