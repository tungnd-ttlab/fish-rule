from typing import TypeVar, Generic, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.constants import DEFAULT_SKIP, DEFAULT_LIMIT

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession) -> None:
        self._model: type[T] = model
        self._session: AsyncSession = session

    async def get(self, id: Any) -> T | None:
        stmt = select(self._model).where(
            self._model.id == id,  # type: ignore[attr-defined]
            self._model.deleted_at.is_(None)  # type: ignore[attr-defined]
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = DEFAULT_SKIP, limit: int = DEFAULT_LIMIT) -> list[T]:
        stmt = (
            select(self._model)
            .where(self._model.deleted_at.is_(None))  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, obj_in: dict[str, Any]) -> T:
        obj = self._model(**obj_in)
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def update(self, id: Any, obj_in: dict[str, Any]) -> T | None:
        obj = await self.get(id)
        if not obj:
            return None
        for key, value in obj_in.items():
            setattr(obj, key, value)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def soft_delete(self, id: Any) -> T | None:
        obj = await self.get(id)
        if not obj:
            return None
        obj.deleted_at = datetime.utcnow()  # type: ignore[attr-defined]
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def commit(self) -> None:
        await self._session.commit()