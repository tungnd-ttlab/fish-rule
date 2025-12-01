from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from domain.entities.user import UserId


@dataclass
class File:
    id: int | None
    user_id: UserId | None
    s3_key: str | None
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None = None

    def __init__(self, id=None, user_id: UUID | None = None, s3_key: HttpUrl | None = None) -> None:
        self.id = id
        self.user_id = UserId(user_id) if user_id else None
        self.s3_key = str(s3_key) if s3_key else None
        self.created_at = datetime.now()
        self.updated_at = None
        self.deleted_at = None