from dataclasses import dataclass
from typing import NewType
from uuid import UUID
from datetime import datetime

from domain.exceptions import UserNotActiveError

UserId = NewType("UserId", UUID)


@dataclass
class User:
    id: UserId
    email: str
    hashed_password: str
    is_active: bool = True
    deleted_at: datetime | None = None

    def ensure_is_active(self) -> None:
        if not self.is_active:
            raise UserNotActiveError
